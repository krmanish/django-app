from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from usr.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for User table to list all not admin user info

    Interact with API with CURL using token based login
    Example:
        GET:
            User List: curl http://localhost:8000/api/users/ -X GET -H "Authorization: Token <token_id>"
            An User Info: curl http://localhost:8000/api/users/<user_id>/ -X GET -H "Authorization: Token <token_id>"
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser, )
    parser_classes = (JSONParser, FormParser, )

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)

    def destroy(self, request, *args, **kwargs):
        """
        Go with soft delete
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
