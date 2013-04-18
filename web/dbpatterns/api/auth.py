from tastypie import http
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse


class DocumentsAuthorization(Authorization):

    def is_authorized(self, request, object=None):

        if request.method == "GET":
            return True

        if request.user.is_anonymous():
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

        return True
