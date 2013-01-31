from django.core.management import BaseCommand

from documents.models import Document

class Command(BaseCommand):

    def handle(self, *args, **options):

        Document.objects.collection.update(
            {"_id": {"$exists": True} },
            {"$set": {"is_public": True}},
                multi=True)