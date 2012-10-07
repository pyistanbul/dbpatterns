from documents.resources import DocumentResource

__author__ = 'fatiherikli'

class DocumentMixin(object):
    """
    The mixin for retrieving Document from MongoDB.
    """
    def get_document(self):
        resource = DocumentResource()
        return resource.obj_get(request=self.request, pk=self.kwargs.get("slug"))