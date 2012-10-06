from django.core.urlresolvers import reverse

def reverse_tastypie_url(resource_name, pk):
    return reverse("api_dispatch_detail", kwargs={
        "resource_name": resource_name,
        "pk": pk
    })