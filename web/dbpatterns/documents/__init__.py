from django.conf import settings

from pymongo import Connection


connection = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)

def get_collection(collection_name):
    return connection[settings.MONGODB_DATABASE][collection_name]