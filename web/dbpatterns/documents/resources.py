from tastypie import fields
from tastypie.authorization import Authorization
from documents.mongodb_resource import MongoDBResource, Document

class DocumentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["delete", "get", "post"]
        authorization = Authorization()
        object_class = Document
        collection = "documents"