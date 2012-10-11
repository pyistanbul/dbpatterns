from django.conf import settings
from pymongo import Connection

db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]

def get_collection(collection_name):
    return db[collection_name]