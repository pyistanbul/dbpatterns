from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, ListView
from documents.forms import DocumentForm
from documents.models import Document
from documents.resources import DocumentResource
from documents.utils import reverse_tastypie_url


class HomeView(TemplateView):
    template_name = "index.html"

class DocumentDetailView(TemplateView):
    template_name = "documents/show.html"

    def get_context_data(self, **kwargs):
        return {
            "document_uri": reverse_tastypie_url("documents", kwargs.get("slug"))
        }


class NewDocumentView(FormView):
    form_class = DocumentForm
    template_name = "documents/new.html"

    def form_valid(self, form):
        resource = DocumentResource()
        self.object_id = resource.get_collection().insert({
            "title": form.cleaned_data.get("title"),
            "user_id": form
        })
        return super(NewDocumentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("edit_document", args=[self.object_id])


class MyDocumentsView(ListView):

    template_name = "documents/list.html"
    context_object_name = "documents"

    def get_queryset(self):
        resource = DocumentResource()
        collection = resource.get_collection().find({"user_id": self.request.user.pk})
        return map(Document, collection)
