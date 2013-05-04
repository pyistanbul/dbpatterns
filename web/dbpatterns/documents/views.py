from datetime import datetime
from itertools import imap

from bson import ObjectId

from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView, FormView, ListView, RedirectView, View
from django.conf import settings
from django import http

from tastypie.http import HttpNoContent

from blog.models import Post
from profiles.mixins import LoginRequiredMixin
from newsfeed.models import Entry
from newsfeed.constants import *
from documents.constants import *
from documents.forms import DocumentForm, ForkDocumentForm, SearchForm
from documents.mixins import DocumentMixin
from documents.models import Document
from documents.resources import DocumentResource
from documents.utils import extract_keywords
from documents.signals import (document_done, fork_done, star_done,
                               document_delete, fork_delete)
from documents.exporters.sql import (MysqlExporter, PostgresExporter,
                                     SQLiteExporter, OracleExporter)


DOCUMENT_EXPORTERS = {
    EXPORTER_MYSQL: MysqlExporter,
    EXPORTER_POSTGRES: PostgresExporter,
    EXPORTER_SQLITE: SQLiteExporter,
    EXPORTER_ORACLE: OracleExporter,
}


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous():
            is_public = True
        else:
            is_public = self.request.GET.get("public") == "true"
        try:
            page_number = int(self.request.GET.get("page"))
        except (ValueError, TypeError):
            page_number = 1

        newsfeed = self.get_newsfeed(
            public=is_public,
            offset=NEWSFEED_LIMIT * (page_number - 1))

        if NEWSFEED_LIMIT * page_number < newsfeed.count():
            next_page_url = self.get_next_page_url(self.request, page_number)
        else:
            next_page_url = None

        return {
            "is_public": is_public,
            "newsfeed": imap(Entry, newsfeed),
            "next_page_url": next_page_url,
            "featured_documents": self.get_featured_documents(),
            "starred_documents": self.get_starred_documents(),
            "latest_posts": self.get_latest_posts(),
            "search_form": SearchForm()
        }

    def get_featured_documents(self):
        return Document.objects.featured()

    def get_starred_documents(self):
        if self.request.user.is_anonymous():
            return []
        return Document.objects.starred(user_id=self.request.user.id)

    def get_newsfeed(self, public=True, offset=0, limit=NEWSFEED_LIMIT):
        """
        Fetches news items from the newsfeed database
        """
        parameters = {
            "news_type": {
                "$in": [NEWS_TYPE_REGISTRATION,
                        NEWS_TYPE_COMMENT,
                        NEWS_TYPE_DOCUMENT,
                        NEWS_TYPE_FORK,
                        NEWS_TYPE_STAR,
                        NEWS_TYPE_FOLLOWING]
            }}

        if not public:
            parameters["recipients"] = {
                "$in": [self.request.user.pk]
            }

        newsfeed = Entry.objects.collection.find(
            parameters).sort([("date_created", -1)])

        return newsfeed[offset:offset + limit]

    def get_next_page_url(self, request, page_number):
        """
        Builds the next page link from GET parameters.
        """
        return "%(newsfeed_url)s?%(parameters)s" % {
            "newsfeed_url": reverse("home"),
            "parameters": urlencode({
                "public": request.GET.get("public") or "false",
                "page": page_number + 1
            })}

    def get_latest_posts(self):
        return Post.objects.all()[:10]


class DocumentDetailView(DocumentMixin, TemplateView):
    template_name = "documents/show.html"

    def get_context_data(self, **kwargs):
        return {"document": self.get_document(),
                "exporters": EXPORTERS}


class ExportDocumentView(DocumentMixin, View):

    def get(self, *args, **kwargs):
        klass = DOCUMENT_EXPORTERS.get(kwargs.get("exporter"))
        if klass is None:
            return http.HttpResponseBadRequest()
        document = self.get_document()
        exporter = klass(document)
        return http.HttpResponse(exporter.as_text(), content_type="text/plain")


class DocumentForksView(DocumentDetailView):
    template_name = "documents/forks.html"

    def get_context_data(self, **kwargs):
        context = super(DocumentForksView, self).get_context_data(**kwargs)
        context["forks"] = context.get("document").forks()
        return context


class DocumentStarsView(DocumentDetailView):
    template_name = "documents/stars.html"


class StarDocumentView(LoginRequiredMixin, RedirectView, DocumentMixin):

    def post(self, request, *args, **kwargs):
        document = self.get_document()
        stars = document.get_stars()
        if request.user.pk in stars:
            stars.remove(request.user.pk)
        else:
            stars.append(request.user.pk)
            star_done.send(sender=self, instance=document,
                           user=request.user)
        Document.objects.collection.update(
            {"_id": document.pk},
            {"$set": {"stars": stars, "star_count": len(stars)}})

        return super(StarDocumentView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse("show_document", args=[self.kwargs.get("slug")])


class DocumentEditView(LoginRequiredMixin, DocumentDetailView):
    template_name = "documents/edit.html"

    def get(self, request, *args, **kwargs):
        if not self.is_authorized():
            return self.redirect()

        return super(DocumentEditView, self).get(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.is_authorized():
            return self.redirect()

        document = self.get_document()

        if document.fork_of is not None:
            signal = fork_delete
        else:
            signal = document_delete

        signal.send(sender=self, instance=self.get_document())

        resource = DocumentResource()
        resource.obj_delete(pk=self.kwargs.get("slug"))

        return HttpNoContent()

    def is_authorized(self):
        return self.get_document().is_editable(user_id=self.request.user.id)

    def redirect(self):
        return http.HttpResponseRedirect(
            reverse("show_document", kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        context = super(DocumentEditView, self).get_context_data(**kwargs)
        context["edit"] = True
        context["FIELD_TYPES"] = FIELD_TYPES
        context["SOCKETIO_HOST"] = settings.SOCKETIO_HOST
        return context


class NewDocumentView(LoginRequiredMixin, FormView):
    form_class = DocumentForm
    template_name = "documents/new.html"

    def form_valid(self, form, **kwargs):
        self.object_id = Document.objects.collection.insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "date_created": datetime.now(),
            "entities": form.cleaned_data.get("entities"),
            "is_public": form.cleaned_data.get("is_public"),
            "_keywords": extract_keywords(form.cleaned_data.get("title"))
        })
        document = Document.objects.get(_id=ObjectId(self.object_id))
        document_done.send(sender=self, instance=document)
        return super(NewDocumentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("edit_document", args=[self.object_id])


class MyDocumentsView(LoginRequiredMixin, TemplateView):
    template_name = "documents/list.html"

    def get_context_data(self, **kwargs):
        return {
            "documents": self.get_documents(),
            "shared": self.get_shared_documents()
        }

    def get_documents(self):
        collection = Document.objects.for_user(self.request.user.id)
        return map(Document, collection)

    def get_shared_documents(self):
        collection = Document.objects.assigned(self.request.user.id)
        return map(Document, collection)


class SearchDocumentView(ListView):
    template_name = "documents/search.html"
    context_object_name = "documents"

    def get_queryset(self):
        form = self.get_form()

        if not form.is_valid():
            return []

        keyword = form.cleaned_data.get("keyword")
        collection = Document.objects.collection.find({
            "_keywords": {"$all": keyword.split()}})

        return map(Document, collection)

    def get_context_data(self, **kwargs):
        return super(SearchDocumentView, self).get_context_data(
            search_form=self.form,
            keyword=self.request.GET.get("keyword"),
            **kwargs)

    def get_form(self):
        self.form = SearchForm(self.request.GET)
        return self.form


class ForkDocumentView(DocumentMixin, NewDocumentView):
    form_class = ForkDocumentForm
    template_name = "documents/fork.html"

    def get_initial(self):
        return {
            "title": self.get_document().title
        }

    def form_valid(self, form, **kwargs):
        document = self.get_document()

        self.object_id = Document.objects.collection.insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "entities": document.entities,
            "fork_of": document.pk,
            "date_created": datetime.now(),
            "is_public": document.is_public,
            "_keywords": extract_keywords(form.cleaned_data.get("title"))
        })

        Document.objects.collection.update(
            {'_id': ObjectId(document.pk)},
            {"$inc": {'fork_count': 1}})

        document = Document.objects.get(_id=ObjectId(self.object_id))
        fork_done.send(sender=self, instance=document)

        return super(NewDocumentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ForkDocumentView, self).get_context_data(**kwargs)
        data["document_id"] = self.get_document()._id
        return data
