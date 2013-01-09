from django.contrib.auth.models import User
from django.core.management import BaseCommand
from pymongo import DESCENDING
from comments.models import Comment
from documents import get_collection
from documents.models import Document
from newsfeed.constants import NEWS_TYPE_REGISTRATION, NEWS_TYPE_DOCUMENT, NEWS_TYPE_FORK, NEWS_TYPE_COMMENT

class Command(BaseCommand):
    """
    A management command for providing initial data for newsfeed.

        - User registrations
        - Documents
        - Forks
        - Comments

    """
    def handle(self, *args, **options):

        newsfeed = get_collection("newsfeed")

        newsfeed.ensure_index([
            ("recipients", DESCENDING),
            ("date_created", DESCENDING),
        ])

        newsfeed.remove()

        for user in User.objects.all():
            newsfeed.insert({
                "object_id": user.id,
                "news_type": NEWS_TYPE_REGISTRATION,
                "date_created": user.date_joined,
                "recipients": [],
                "sender": {
                    "username": user.username,
                    "email": user.email # it's required for gravatar
                },
            })


        for document in map(Document, get_collection("documents").find()):
            news_type = NEWS_TYPE_DOCUMENT if document.fork_of else NEWS_TYPE_FORK
            newsfeed.insert({
                "object_id": document.pk,
                "news_type": news_type,
                "date_created": document.date_created,
                "recipients": [],
                "sender": {
                    "username": document.user.username,
                    "email": document.user.email # it's required for gravatar
                },
            })

        for comment in map(Comment, get_collection("comments").find()):
            newsfeed.insert({
                "object_id": comment.pk,
                "news_type": NEWS_TYPE_COMMENT,
                "date_created": comment.date_created,
                "recipients": [],
                "sender": {
                    "username": comment.user.username,
                    "email": comment.user.email # it's required for gravatar
                },
            })

        print get_collection("newsfeed").count()