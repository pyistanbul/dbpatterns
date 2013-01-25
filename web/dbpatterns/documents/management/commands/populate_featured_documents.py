from django.core.management import BaseCommand

from documents.models import Document


class Command(BaseCommand):
    """
    Populates featured documents
    """
    def handle(self, *args, **options):

        Document.objects.collection.update(
            {"fork_count": {"$gt": 1}},
            {"$set": {"is_featured": True}
        }, multi=True)