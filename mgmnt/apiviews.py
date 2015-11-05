from imdb.imdb_filters import MoviesFilter
from imdb.imdb_permissions import IMDBUserPermission
from mgmnt.models import Directors, Genres, Movies
from mgmnt.serializers import (
    DirectorsSerializer,
    GenresSerializer,
    MoviesSerializer,
)
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response


class MovieViewSet(viewsets.ModelViewSet):
    """
    Viewset for movies info for list/retrieve/delete/update
    Allow search by name

    Interact with API with CURL using token based login
    Example:
        GET:
            Movies List: curl http://localhost:8000/api/movies/ -X GET -H "Authorization: Token <token_id>"
            A Movie Info: curl http://localhost:8000/api/movies/<movie_id>/ -X GET -H "Authorization: Token <token_id>"
        Search:
            curl http://localhost:8000/api/movies/?genre_name=Adventure\&popularity=83.00 -X GET -H "Authorization: Token <token_id>"
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (IMDBUserPermission, )

    serializer_class = MoviesSerializer
    queryset = Movies.get_all_movies()
    filter_backends = (DjangoFilterBackend, )
    filter_class = MoviesFilter

    def destroy(self, request, *args, **kwargs):
        """
        Go with soft delete
        """
        instance = self.get_object()
        instance.is_deleted = True  # Mark soft delete
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreListView(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Genres info for list and retrieve

    Interact with API with CURL
    Example:
        GET:
            Genre List: curl http://localhost:8000/api/genres/ -X GET -H "Authorization: Token <token_id>"
            A Genre Info: curl http://localhost:8000/api/genres/<genre_id>/ -X GET -H "Authorization: Token <token_id>"
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = GenresSerializer
    queryset = Genres.objects.all()


class DirectorListView(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Directors info for list and retrieve

    Interact with API with CURL
    Example:
        GET:
            Director list: curl http://localhost:8000/api/directors/ -X GET -H "Authorization: Token <token_id>"
            A Director info: curl http://localhost:8000/api/directors/<director_id>/ -X GET -H "Authorization: Token <token_id>"
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = DirectorsSerializer
    queryset = Directors.objects.all()
