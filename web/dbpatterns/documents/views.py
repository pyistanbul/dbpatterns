from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, ListView, RedirectView, View
from django import http

from tastypie.http import HttpNoContent

from auth.mixins import LoginRequiredMixin
from documents import get_collection
from documents.constants import FIELD_TYPES, EXPORTER_ORACLE, EXPORTER_SQLITE, EXPORTER_POSTGRES, EXPORTER_MYSQL, EXPORTERS
from documents.exporters.sql import MysqlExporter, PostgresExporter, SQLiteExporter, OracleExporter
from documents.forms import DocumentForm, ForkDocumentForm, SearchForm
from documents.mixins import DocumentMixin
from documents.models import Document
from documents.resources import DocumentResource
from documents.utils import extract_keywords

DOCUMENT_EXPORTERS = {
    EXPORTER_MYSQL: MysqlExporter,
    EXPORTER_POSTGRES: PostgresExporter,
    EXPORTER_SQLITE: SQLiteExporter,
    EXPORTER_ORACLE: OracleExporter
}

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        documents = get_collection("documents")
        featured_documents = map(Document, documents.find({
           "featured": True
        }))
        most_rated_documents = map(Document,
            documents.find().sort([("star_count", -1)]).limit(9))
        recently_added_documents = map(Document,
            documents.find({
                "$where": "this.entities && this.entities.length > 1"
            }).sort([("date_created", -1)]).limit(9))
        return {
            "featured_documents": featured_documents,
            "most_rated_documents": most_rated_documents,
            "recently_added_documents": recently_added_documents,
            "search_form": SearchForm()
        }

class DocumentDetailView(DocumentMixin, TemplateView):
    template_name = "documents/show.html"

    def get_context_data(self, **kwargs):
        return {
            "document": self.get_document(),
            "exporters": EXPORTERS
        }


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

        resource = DocumentResource()
        resource.obj_update(bundle=resource.build_bundle(data={
            "stars": stars,
            "star_count": len(stars)
        }), pk=document.pk)

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

        resource = DocumentResource()
        resource.obj_delete(pk=self.kwargs.get("slug"))
        return HttpNoContent()

    def is_authorized(self):
        return self.get_document().get_user() == self.request.user

    def redirect(self):
        return http.HttpResponseRedirect(reverse("show_document", kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        context = super(DocumentEditView, self).get_context_data(**kwargs)
        context["edit"] = True
        context["FIELD_TYPES"] = FIELD_TYPES
        return context



class NewDocumentView(LoginRequiredMixin, FormView):
    form_class = DocumentForm
    template_name = "documents/new.html"

    def form_valid(self, form, **kwargs):
        self.object_id = get_collection("documents").insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "date_created": datetime.now(),
            "entities": form.cleaned_data.get("entities"),
            "_keywords": extract_keywords(form.cleaned_data.get("title"))
        })
        return super(NewDocumentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("edit_document", args=[self.object_id])


class MyDocumentsView(LoginRequiredMixin, ListView):

    template_name = "documents/list.html"
    context_object_name = "documents"

    def get_queryset(self):
        collection = get_collection("documents").find({"user_id": self.request.user.pk})
        return map(Document, collection)


class SearchDocumentView(ListView):

    template_name = "documents/search.html"
    context_object_name = "documents"

    def get_queryset(self):

        form = self.get_form()

        if not form.is_valid():
            return []

        keyword = form.cleaned_data.get("keyword")

        collection = get_collection("documents").find({
            "_keywords": {
                "$all": keyword.split()
            }
        })

        return map(Document, collection)

    def get_context_data(self, **kwargs):
        return super(SearchDocumentView, self).get_context_data(
            search_form = self.form,
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
        resource = DocumentResource()
        document = self.get_document()
        self.object_id = get_collection("documents").insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "entities": document.entities,
            "fork_of": document.pk,
            "date_created": datetime.now(),
            "_keywords": extract_keywords(form.cleaned_data.get("title"))
        })

        # TODO: use atomic operations for incrementing!
        resource.obj_update(bundle=resource.build_bundle(data={
            "fork_count": (document.fork_count or 0) + 1
        }), pk=document.pk)

        return super(NewDocumentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ForkDocumentView, self).get_context_data(**kwargs)
        data["document_id"] = self.get_document()._id
        return data