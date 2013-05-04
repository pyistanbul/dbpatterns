from datetime import datetime
from bson import ObjectId

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver

from tastypie import fields, http
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse

from api.resources import MongoDBResource
from comments.constants import COMMENT_TEMPLATE
from comments.models import Comment
from comments.signals import comment_done, comment_delete
from documents import get_collection


class CommentResource(MongoDBResource):
    id = fields.CharField(attribute="_id")
    body = fields.CharField(attribute="body", null=True)
    document_id = fields.CharField(
        attribute="document_id", readonly=True, null=True)
    date_created = fields.DateTimeField(
        attribute="date_created", readonly=True, null=True)

    # profile specific fields
    user_id = fields.IntegerField(attribute="user_id", readonly=True, null=True)
    username = fields.CharField(attribute="username", readonly=True, null=True)
    profile_url = fields.CharField(
        attribute="profile_url", readonly=True, null=True)
    avatar_url = fields.CharField(
        attribute="avatar_url", readonly=True, null=True)

    class Meta:
        resource_name = "comments"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "delete"]
        authorization = Authorization()
        object_class = Comment
        always_return_data = True

    def dehydrate(self, bundle):
        """
        Injects `has_delete_permission` field which indicates the user is
        authorized to remove comment or not.
        """
        if bundle.request is not None and bundle.request.user.is_authenticated():
            bundle.data["has_delete_permission"] = \
                bundle.request.user.pk == bundle.data.get("user_id")
        return bundle

    def get_collection(self):
        return get_collection("comments")

    def obj_get_list(self, request=None, **kwargs):
        """
        Returns comment of the document
        """
        if not "document_id" in kwargs:
            return super(CommentResource, self).obj_get_list(request, **kwargs)

        comments = self.get_collection().find({
            "document_id": kwargs.get("document_id")
        }).sort([['_id', 1]])

        return map(self.get_object_class(), comments)

    def obj_delete(self, request=None, **kwargs):
        """
        - Removes comment if user is authorized
        - Fires comment_delete signal
        """
        comment = self.obj_get(**kwargs)
        if (request.user.is_anonymous() or
                not request.user.pk == comment.get("user_id")):
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        super(CommentResource, self).obj_delete(request, **kwargs)

        comment_delete.send(
            sender=self,
            comment_id=comment.id,
            instance=comment
        )

    def obj_create(self, bundle, request=None, **kwargs):
        """
        - Creates new comment
        - Fires comment_done signal
        """
        bundle = super(CommentResource, self).obj_create(
            bundle,
            user_id=request.user.id,
            document_id=kwargs.get("document_id"),
            date_created=datetime.now()
        )

        comment_id = bundle.obj
        comment = Comment.objects.get(_id=ObjectId(comment_id))

        comment_done.send(
            sender=self,
            comment_id=comment_id,
            instance=comment
        )

        bundle.obj = comment

        return bundle


@receiver(comment_done)
def comment_on(sender, comment_id, **kwargs):
    """
    Sends an email to the author of the commented document
    """
    comment = Comment(get_collection("comments").find_one({
        "_id": ObjectId(comment_id)
    }))

    document = comment.document

    send_mail(
        subject="You have new comment(s) on your pattern",
        message=COMMENT_TEMPLATE % {
            "document_title": document.title,
            "document_link": settings.SITE_URL + document.get_absolute_url()
        },
        from_email=settings.COMMENTS_FROM_EMAIL,
        recipient_list=['"%s" <%s>' % (
            document.user.get_full_name() or document.user.username,
            document.user.email)],
        fail_silently=True
    )