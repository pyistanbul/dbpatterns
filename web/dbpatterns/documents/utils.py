from topia.termextract import extract

from django.core.urlresolvers import reverse


extractor = extract.TermExtractor()
extractor.filter = extract.permissiveFilter

def reverse_tastypie_url(resource_name, pk):
    return reverse("api_dispatch_detail", kwargs={
        "resource_name": resource_name,
        "pk": pk
    })

def extract_keywords(title):
    return [term.lower() for term, _, _, in extractor(title)]