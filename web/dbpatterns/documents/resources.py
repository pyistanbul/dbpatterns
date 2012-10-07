from tastypie import fields
from api.auth import DocumentsAuthorization
from api.resources import MongoDBResource

from documents.models import Document


class DocumentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)
    user_id = fields.CharField(attribute="user_id", readonly=True, null=True)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "put"]
        authorization = DocumentsAuthorization()
        object_class = Document
        collection = "documents"

    def obj_sort(self, orderings, limit=20):
        return map(Document, self.get_collection().find().sort(orderings).limit(limit))

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Creates mongodb document from POST data.
        """
        return super(DocumentResource, self).obj_create(bundle,
            user_id=request.user.pk)

