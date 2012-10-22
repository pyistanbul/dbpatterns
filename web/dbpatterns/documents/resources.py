from django.conf.urls import url
from tastypie import http
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.utils import trailing_slash

from api.auth import DocumentsAuthorization
from api.resources import MongoDBResource
from comments.resources import CommentResource

from documents import get_collection
from documents.models import Document


class DocumentResource(MongoDBResource):

    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)
    user_id = fields.IntegerField(attribute="user_id", readonly=True, null=True)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "put"]
        authorization = DocumentsAuthorization()
        object_class = Document

    def get_collection(self):
        return get_collection("documents")

    def obj_create(self, bundle, request=None, **kwargs):
        return super(DocumentResource, self).obj_create(bundle,
            user_id=request.user.pk)

    def obj_update(self, bundle, request=None, **kwargs):

        if request is not None and \
           self.obj_get(pk=kwargs.get("pk")).user_id != request.user.pk:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        return super(DocumentResource, self).obj_update(bundle, request, **kwargs)

    # nested resources

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/comments%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_comments'), name="api_get_comments"),
        ]

    def dispatch_comments(self, request, **kwargs):
        obj = Document(self.cached_obj_get(request=request,
            **self.remove_api_resource_names(kwargs)))
        child_resource = CommentResource()
        return child_resource.dispatch_list(request, document_id=obj.pk)