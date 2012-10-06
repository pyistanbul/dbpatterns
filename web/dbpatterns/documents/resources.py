from tastypie import fields
from tastypie.authorization import Authorization
from api.resources import MongoDBResource, Document

class DocumentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)
    user_id = fields.CharField(attribute="user_id", readonly=True, null=True)

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Creates mongodb document from POST data.
        """
        return super(DocumentResource, self).obj_create(bundle,
            user_id=request.user.pk)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["delete", "get", "post"]
        authorization = Authorization()
        object_class = Document
        collection = "documents"