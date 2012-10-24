from datetime import datetime
from bson import ObjectId

from tastypie import fields
from tastypie.authorization import Authorization

from api.resources import MongoDBResource
from comments.models import Comment
from documents import get_collection

class CommentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    body = fields.CharField(attribute="body", null=True)
    document_id = fields.CharField(attribute="document_id", readonly=True, null=True)
    date_created = fields.DateTimeField(attribute="date_created", readonly=True, null=True)

    # profile specific fields
    user_id = fields.CharField(attribute="user_id", readonly=True, null=True)
    username = fields.CharField(attribute="username", readonly=True, null=True)
    profile_url = fields.CharField(attribute="profile_url", readonly=True, null=True)
    avatar_url = fields.CharField(attribute="avatar_url", readonly=True, null=True)

    class Meta:
        resource_name = "comments"
        list_allowed_methods = ["delete", "get", "post"]
        detail_allowed_methods = ["get", "put", "delete"]
        authorization = Authorization()
        object_class = Comment

    def dehydrate(self, bundle):
        if bundle.request is not None:
            bundle.data["has_delete_permission"] = \
                str(bundle.request.user.pk) == bundle.data.get("user_id")
        return bundle

    def get_collection(self):
        return get_collection("comments")

    def obj_get_list(self, request=None, **kwargs):
        return map(self.get_object_class(), self.get_collection().find({
            "document_id": kwargs.get("document_id")
        }).sort([['_id', 1]]))

    def obj_create(self, bundle, request=None, **kwargs):
        return super(CommentResource, self).obj_create(bundle,
            user_id=request.user.id,
            document_id=kwargs.get("document_id"),
            date_created=datetime.now()
        )