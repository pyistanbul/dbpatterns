from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, ListView, RedirectView

from tastypie.http import HttpNoContent
from auth.mixins import LoginRequiredMixin

from documents.forms import DocumentForm
from documents.mixins import DocumentMixin
from documents.models import Document
from documents.resources import DocumentResource


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        resource = DocumentResource()
        most_rated_documents = resource.obj_sort([("star_count", -1)], limit=8)
        return {
            "most_rated_documents": most_rated_documents
        }

class DocumentDetailView(DocumentMixin, TemplateView):
    template_name = "documents/show.html"

    def get_context_data(self, **kwargs):
        return {
            "document": self.get_document()
        }

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
        return HttpResponseRedirect(reverse("show_document", kwargs=self.kwargs))


class NewDocumentView(LoginRequiredMixin, FormView):
    form_class = DocumentForm
    template_name = "documents/new.html"

    def form_valid(self, form, **kwargs):
        resource = DocumentResource()
        self.object_id = resource.get_collection().insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "date_created": datetime.now()
        })
        return super(NewDocumentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("edit_document", args=[self.object_id])


class MyDocumentsView(LoginRequiredMixin, ListView):

    template_name = "documents/list.html"
    context_object_name = "documents"

    def get_queryset(self):
        resource = DocumentResource()
        collection = resource.get_collection().find({"user_id": self.request.user.pk})
        return map(Document, collection)


class ForkDocumentView(DocumentMixin, NewDocumentView):
    form_class = DocumentForm
    template_name = "documents/fork.html"

    def get_initial(self):
        return {
            "title": self.get_document().title
        }

    def form_valid(self, form, **kwargs):
        resource = DocumentResource()
        document = self.get_document()
        self.object_id = resource.get_collection().insert({
            "title": form.cleaned_data.get("title"),
            "user_id": self.request.user.pk,
            "entities": document.entities,
            "fork_of": document.pk,
            "date_created": datetime.now()
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