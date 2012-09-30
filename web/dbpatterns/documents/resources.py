
import json
from bson import ObjectId
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from pymongo import Connection
from tastypie import fields, bundle

from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource, ModelResource

db = Connection().dbpatterns


class DummyObject(dict):
    __getattr__ = dict.get

class DocumentResource(Resource):

    id = fields.CharField(attribute="_id")
    title = fields.CharField(attribute="title", null=True)
    entities = fields.ListField(attribute="entities", null=True)

    class Meta:
        resource_name = "documents"
        list_allowed_methods = ["delete", "get", "post"]
        authorization = Authorization()
        object_class = DummyObject

    def get_object_list(self, request):
        return map(DummyObject, db.documents.find())

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        return DummyObject(db.documents.find_one({
            "_id": ObjectId(kwargs.get("pk"))
        }))

    def obj_create(self, bundle, **kwargs):
        db.documents.insert(bundle.data)
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        db.documents.update({
            "_id": ObjectId(kwargs.get("pk"))
        }, {
            "$set": bundle.data
        })
        return bundle

    def obj_delete_list(self, request=None, **kwargs):
        db.documents.remove()

    def get_resource_uri(self, item):
        if isinstance(item, Bundle):
            pk = item.obj._id
        else:
            pk = item._id
        return reverse("api_dispatch_detail", kwargs={
            "resource_name": self._meta.resource_name,
            "pk": pk
        })