from bson import ObjectId

from tastypie import fields
from tastypie.authorization import Authorization

from api.resources import MongoDBResource
from comments.models import Comment
from documents import get_collection

class CommentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    body = fields.CharField(attribute="body", null=True)
    user_id = fields.IntegerField(attribute="user_id", readonly=True, null=True)
    document_id = fields.CharField(attribute="document_id", readonly=True, null=True)
    profile_url = fields.CharField(attribute="profile_url", readonly=True, null=True)
    avatar_url = fields.CharField(attribute="avatar_url", readonly=True, null=True)

    class Meta:
        resource_name = "comments"
        list_allowed_methods = ["delete", "get", "post"]
        detail_allowed_methods = ["get", "put", "delete"]
        authorization = Authorization()
        object_class = Comment

    def get_collection(self):
        return get_collection("comments")

    def obj_get_list(self, request=None, **kwargs):
        return map(self.get_object_class(), self.get_collection().find({
            "document_id": kwargs.get("document_id")
        }))

    def obj_create(self, bundle, request=None, **kwargs):
        return super(CommentResource, self).obj_create(bundle,
            user_id=request.user.id, document_id=kwargs.get("document_id"))