from django.core.urlresolvers import reverse

class Document(dict):
    __getattr__ = dict.get

    def get_absolute_url(self):
        return reverse("show_document", args=[self._id])