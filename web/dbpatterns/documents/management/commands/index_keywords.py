from django.core.management import BaseCommand

from documents import get_collection
from documents.utils import extract_keywords


class Command(BaseCommand):

    def handle(self, *args, **options):

        get_collection("documents").ensure_index([
                ("_keywords", 1),
                ("title", 1),
            ])

        for document in get_collection("documents").find():

            print document.get("_id")

            get_collection("documents").update({
                "_id": document.get("_id")
            }, {
                "$set": {
                    "_keywords": extract_keywords(document.get("title"))
                }
            })