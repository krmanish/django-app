from imdb.imdb_filters import DirectorsFilter, GenresFilter, MoviesFilter
from imdb.imdb_permissions import IMDBUserPermission
from mgmnt.models import Directors, Genres, Movies
from mgmnt.serializers import (
    CreateUpdateMovieSerializer,
    DirectorsSerializer,
    GenresSerializer,
    MoviesSerializer,
)
from rest_framework import status, viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response


class IMDBUserPermission(viewsets.ModelViewSet):
    """
    Base model view class with all required info
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
            Movies List: curl http://drftest.herokuapp.com/api/movies/ -X GET -H "Authorization: Token <token_id>"
            A Movie Info: curl http://drftest.herokuapp.com/api/movies/<movie_id>/ -X GET -H "Authorization: Token <token_id>"
            Retrieve:
                curl http://drftest.herokuapp.com/api/movies/501/ -X GET  -H "Authorization: Token <token_id>"
        POST:
            Create:
                curl http://drftest.herokuapp.com/api/movies/ -X POST
                -d '{"genre": <list of genre>, "director": <genre_name>, "name": <movie_name>, "imdb_score": <imdb_score>}'
                -H "Authorization: Token <token_id>" -H "Content-Type: application/json"
        PUT/PATCH: Always Accept complete update
            curl http://drftest.herokuapp.com/api/movies/501/ -X PUT
            d '{"genre": <list of genre>, "director": <genre_name>, "name": <movie_name>, "imdb_score": <imdb_score>}'
            -H "Authorization: Token <token_id>" -H "Content-Type: application/json"
        Search:
            curl http://drftest.herokuapp.com/api/movies/?genre_name=Adventure\&imdb_score=8.0 -X GET
            -H "Authorization: Token <token_id>"
    """

    queryset = Movies.get_all_movies()
    filter_class = MoviesFilter

    def get_serializer_class(self):
        """
        Get serializer class
        """
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CreateUpdateMovieSerializer
        else:
            return MoviesSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve movie record
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'name': serializer.data['name'],
            'director': serializer.data['director_name'],
            'genre': serializer.data['genre_list'],
            'imdb_score': serializer.data['imdb_score'],
            'popularity': serializer.data['popularity'],
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update record using partial
        """
        partial = False
        api_response_dict = {'success': False, 'errors': [], 'message': ''}
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            data = serializer._validated_data
            try:
                Movies.objects.save_with_related(data, movie_obj=instance)
                api_response_dict.update({
                    'message': "Data updated successfully!",
                    'status': True,
                    'data': data})
                return Response(api_response_dict, status=status.HTTP_200_OK)
            except Exception as err:
                api_response_dict.uppdate({'message': 'Error: System error, please try after sometime'})

        api_response_dict['errors'] = serializer.errors
        return Response(api_response_dict, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Override create views
        """
        api_response_dict = {'success': False, 'errors': [], 'message': ''}
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            data = serializer.data
            data['user'] = request.user
            try:
                Movies.objects.save_with_related(data)
                api_response_dict.update({
                    'message': "Data saved in our system successfully!",
                    'status': True,
                    'data': serializer.data})
                return Response(api_response_dict, status=status.HTTP_201_CREATED)

            except Exception as err:
                api_response_dict.uppdate({'message': 'Error: System error, please try after sometime'})

        api_response_dict['errors'] = serializer.errors
        return Response(api_response_dict, status=status.HTTP_400_BAD_REQUEST)


class GenreListView(IMDBUserPermission):
    """
    Viewset for Genres info for list/retrieve/delete/update

    Interact with API with CURL
    Example:
        GET:
            Genre List: curl http://drftest.herokuapp.com/api/genres/ -X GET -H "Authorization: Token <token_id>"
            A Genre Info: curl http://drftest.herokuapp.com/api/genres/<genre_id>/ -X GET -H "Authorization: Token <token_id>"
        POST:
            With Json Data: curl http://drftest.herokuapp.com/api/genres/ -X POST -d '{"genre": "<genre_name>"}'
                -H "Authorization: Token <token_id>" -H "Content-Type: application/json"
            With Form Data: curl http://drftest.herokuapp.com/api/genres/ -X POST -d 'genre=<genre_name>'
                -H "Authorization: Token <token_id>"
        PUT:
            curl http://drftest.herokuapp.com/api/genres/<genre_id>/ -X PUT -d 'genre=<genre_name>'
            -H "Authorization: Token <token_id>"
        Search:
            curl http://drftest.herokuapp.com/api/genres/?genre=<name_text> -X GET -H "Authorization: Token <token_id>"
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
            Director list: curl http://drftest.herokuapp.com/api/directors/ -X GET -H "Authorization: Token <token_id>"
            A Director info: curl http://drftest.herokuapp.com/api/directors/<director_id>/ -X GET -H "Authorization: Token <token_id>"
        POST:
            curl http://drftest.herokuapp.com/api/directors/ -X POST -d '{"full_name": <full_name>}'
            -H "Authorization: Token <token_id>" -H "Content-Type: application/json"
        PUT:
            curl http://drftest.herokuapp.com/api/directors/<genre_id>/ -X PUT -d '{"full_name": <genre_name>}'
            -H "Authorization: Token <token_id>"  -H "Content-Type: application/json"
        Search:
            curl http://drftest.herokuapp.com/api/directors/?name=<name_text> -X GET -H "Authorization: Token <token_id>"
    """

    serializer_class = DirectorsSerializer
    queryset = Directors.get_all()
    filter_class = DirectorsFilter
