import operator
from bson import ObjectId

from django.conf.urls import url
from django.core.urlresolvers import reverse

from tastypie import http
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.utils import trailing_slash

from api.auth import DocumentsAuthorization
from api.resources import MongoDBResource
from comments.resources import CommentResource
from documents import get_collection
from documents.models import Document
from documents.signals import assignment_done


class DocumentResource(MongoDBResource):
    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)
    user_id = fields.IntegerField(attribute="user_id", readonly=True, null=True)
    is_public = fields.BooleanField(attribute="is_public", null=True)
    assignees = fields.ListField(attribute="assignees", null=True)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "put"]
        authorization = DocumentsAuthorization()
        object_class = Document

    def get_collection(self):
        return get_collection("documents")

    def obj_get(self, request=None, **kwargs):
        """
        Returns mongodb document from provided id.
        """
        document = Document.objects.get(_id=ObjectId(kwargs.get("pk")))

        if request is not None and not document.is_visible(user_id=request.user.id):
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        return document

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Populates the id of user to create document.
        """
        return super(DocumentResource, self).obj_create(
            bundle, user_id=request.user.pk)

    def obj_update(self, bundle, request=None, **kwargs):
        """
        - Checks the permissions of user, and updates the document
        - Fires assignmend_done signals for assigned users
        """
        document = self.obj_get(request=request, pk=kwargs.get("pk"))

        if not document.is_editable(user_id=request.user.id):
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        bundle = super(DocumentResource, self).obj_update(
            bundle, request, **kwargs)

        updated_document = self.obj_get(request=request, pk=kwargs.get("pk"))
        if document.assignees != updated_document.assignees:
            original = map(operator.itemgetter("id"), document.assignees)
            updated = map(operator.itemgetter("id"), updated_document.assignees)
            for user_id in set(updated).difference(original):
                assignment_done.send(
                    sender=self,
                    user_id=user_id,
                    instance=updated_document)

        return bundle

    def dehydrate(self, bundle):
        """
        Inserts the comments uri to the document bundle
        """
        bundle.data["comments_uri"] = reverse("api_get_comments", kwargs={
            "resource_name": "documents",
            "pk": bundle.data.get("id")
        })
        return bundle

    def override_urls(self):
        """
        Adds the urls of nested resources
        """
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/comments%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_comments'), name="api_get_comments"),
        ]

    def dispatch_comments(self, request, **kwargs):
        document = Document(self.cached_obj_get(
            request=request, **self.remove_api_resource_names(kwargs)))
        child_resource = CommentResource()
        return child_resource.dispatch_list(request, document_id=document.pk)
