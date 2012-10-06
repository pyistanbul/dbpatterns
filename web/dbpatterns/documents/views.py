from django.core.urlresolvers import reverse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"

class DocumentView(TemplateView):
    template_name = "documents/show.html"

    def get_context_data(self, **kwargs):
        document_uri = reverse("api_dispatch_detail", kwargs={
            "resource_name": "documents",
            "pk": kwargs.get("slug")
        })
        return {
            "document_uri": document_uri
        }