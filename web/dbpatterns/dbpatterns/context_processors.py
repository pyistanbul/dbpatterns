from django.conf import settings

def assets_version(request):
    return {
        "ASSETS_VERSION": settings.ASSETS_VERSION
    }