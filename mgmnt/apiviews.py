from imdb.imdb_filters import DirectorsFilter, GenresFilter, MoviesFilter
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
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response


class IMDBUserPermission(viewsets.ModelViewSet):
    """
    Maintain the user permission
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    permission_classes = (IMDBUserPermission, )
    parser_classes = (JSONParser, FormParser, )
    filter_backends = (DjangoFilterBackend, )

    def destroy(self, request, *args, **kwargs):
        """
        Go with soft delete
        """
        instance = self.get_object()
        instance.is_active = False

        # For movie record
        if hasattr(instance, 'is_deleted'):
            instance.is_deleted = True

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieViewSet(IMDBUserPermission):
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

    serializer_class = MoviesSerializer
    queryset = Movies.get_all_movies()
    filter_class = MoviesFilter


class GenreListView(IMDBUserPermission):
    """
    Viewset for Genres info for list/retrieve/delete/update

    Interact with API with CURL
    Example:
        GET:
            Genre List: curl http://localhost:8000/api/genres/ -X GET -H "Authorization: Token <token_id>"
            A Genre Info: curl http://localhost:8000/api/genres/<genre_id>/ -X GET -H "Authorization: Token <token_id>"
        POST:
            With Json Data: curl http://localhost:8000/api/genres/ -X POST -d '{"genre": "<genre_name>"}'
                -H "Authorization: Token 15e42b6b6f9d331cd051d93e6e1095e709a6508b" -H "Content-Type: application/json"
            With Form Data: curl http://localhost:8000/api/genres/ -X POST -d 'genre=<genre_name>'
                -H "Authorization: Token 15e42b6b6f9d331cd051d93e6e1095e709a6508b"
        PUT:
            curl http://localhost:8000/api/genres/<genre_id>/ -X PUT -d 'genre=<genre_name>'
            -H "Authorization: Token 15e42b6b6f9d331cd051d93e6e1095e709a6508b"
        Search:
            Search:
            curl http://localhost:8000/api/genres/?genre=<name_text> -X GET -H "Authorization: Token <token_id>"
    """
    serializer_class = GenresSerializer
    queryset = Genres.get_all()
    filter_class = GenresFilter


class DirectorListView(IMDBUserPermission):
    """
    Viewset for Directors info for list/retrieve/delete/update

    Interact with API with CURL
    Example:
        GET:
            Director list: curl http://localhost:8000/api/directors/ -X GET -H "Authorization: Token <token_id>"
            A Director info: curl http://localhost:8000/api/directors/<director_id>/ -X GET -H "Authorization: Token <token_id>"
        Search:
            curl http://localhost:8000/api/directors/?name=<name_text> -X GET -H "Authorization: Token <token_id>"
    """

    serializer_class = DirectorsSerializer
    queryset = Directors.get_all()
    filter_class = DirectorsFilter
