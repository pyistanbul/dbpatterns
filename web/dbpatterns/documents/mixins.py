from bson.errors import InvalidId
from django.http import Http404

from documents.resources import DocumentResource


class DocumentMixin(object):
    """
    The mixin for retrieving Document from MongoDB.
    """
    def get_document(self):
        resource = DocumentResource()
        try:
            return resource.obj_get(request=self.request, pk=self.kwargs.get("slug"))
        except (TypeError, InvalidId):
            raise Http404("Document is not found.")