import re
from nltk import WordNetLemmatizer, LancasterStemmer
from django.core.urlresolvers import reverse

wordnet_lemmatizer = WordNetLemmatizer()
lancaster_stemmer = LancasterStemmer()

def extract_keywords(title):

    original_keywords = [keyword.lower() for keyword in re.split('\W+', title)]

    lemmatized_keywords =  map(wordnet_lemmatizer.lemmatize, original_keywords)

    stemmed_keywords = map(lancaster_stemmer.stem, original_keywords)

    print stemmed_keywords

    return list(set(original_keywords + lemmatized_keywords + stemmed_keywords))


def reverse_tastypie_url(resource_name, pk):
    return reverse("api_dispatch_detail", kwargs={
        "resource_name": resource_name,
        "pk": pk
    })

