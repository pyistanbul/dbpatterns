from bson import ObjectId

from comments.models import Comment
from documents.models import Document
from newsfeed.constants import NEWS_TYPE_COMMENT, NEWS_TYPE_DOCUMENT, NEWS_TYPE_FORK

RELATED_MODELS = {
    NEWS_TYPE_COMMENT: Comment,
    NEWS_TYPE_DOCUMENT: Document,
    NEWS_TYPE_FORK: Document
}

class Entry(dict):
    """
    A model that wraps mongodb document
    """
    @property
    def related_object(self):
        news_type = self.get("news_type")
        object_id = self.get("object_id")
        model = RELATED_MODELS.get(news_type)

        if model:
            return model.objects.get(_id=ObjectId(object_id))