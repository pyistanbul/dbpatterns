import re
import logging

from nltk import WordNetLemmatizer, LancasterStemmer

from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)
wordnet_lemmatizer = WordNetLemmatizer()
lancaster_stemmer = LancasterStemmer()


def extract_keywords(title):
    original_keywords = [keyword.lower() for keyword in re.split('\W+', title)]

    try:
        lemmatized_keywords = map(wordnet_lemmatizer.lemmatize,
                                  original_keywords)
    except LookupError:
        logging.error('Please install corpora/wordnet dictionary')
        return []

    stemmed_keywords = map(lancaster_stemmer.stem, original_keywords)

    return list(set(original_keywords
                    + lemmatized_keywords
                    + stemmed_keywords))


def reverse_tastypie_url(resource_name, pk=None):
    """
    Returns tastypie url
    """
    if pk is None:
        return reverse("api_dispatch_list", args=[resource_name])

    return reverse("api_dispatch_detail", kwargs={
        "resource_name": resource_name,
        "pk": pk})
