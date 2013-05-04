from bson import ObjectId
from pymongo import Connection

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf import settings

from tastypie.bundle import Bundle
from tastypie.resources import Resource


class Document(dict):
    # dictionary-like object for mongodb documents.
    __getattr__ = dict.get


class MongoDBResource(Resource):
    """
    A base resource that allows to make CRUD operations for mongodb.
    """

    def get_object_class(self):
        return self._meta.object_class

    def get_collection(self):
        """
        Encapsulates collection name.
        """
        raise NotImplementedError("You should implement get_collection method.")

    def obj_get_list(self, request=None, **kwargs):
        """
        Maps mongodb documents to Document class.
        """
        return map(self.get_object_class(), self.get_collection().find())

    def obj_get(self, request=None, **kwargs):
        """
        Returns mongodb document from provided id.
        """
        return self.get_object_class()(self.get_collection().find_one({
            "_id": ObjectId(kwargs.get("pk"))
        }))

    def obj_create(self, bundle, **kwargs):
        """
        Creates mongodb document from POST data.
        """
        bundle.data.update(kwargs)
        bundle.obj = self.get_collection().insert(bundle.data)
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        """
        Updates mongodb document.
        """
        self.get_collection().update(
            {"_id": ObjectId(kwargs.get("pk"))},
            {"$set": bundle.data})
        return bundle

    def obj_delete_list(self, request=None, **kwargs):
        """
        Removes all documents from collection
        """
        self.get_collection().remove()

    def obj_delete(self, request=None, **kwargs):
        """
        Removes single document from collection
        """
        parameters = {"_id": ObjectId(kwargs.get("pk"))}
        self.get_collection().remove(parameters)

    def get_resource_uri(self, item):
        """
        Returns resource URI for bundle or object.
        """
        if isinstance(item, Bundle):
            if isinstance(item.obj, ObjectId):
                pk = str(item.obj)
            else:
                pk = item.obj._id
        else:
            pk = item._id
        return reverse("api_dispatch_detail", kwargs={
            "resource_name": self._meta.resource_name,
            "pk": pk
        })