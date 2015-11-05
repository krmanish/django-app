from mgmnt.models import Directors, Genres, Movies
from rest_framework import serializers


class MoviesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Movies serializer
    """

    class Meta:
        model = Movies
        fields = ('name', 'imdb_score', 'popularity', 'director', 'genre')


class DirectorsSerializer(serializers.ModelSerializer):
    """
    Movies serializer
    """

    class Meta:
        model = Directors
        fields = ('full_name', )


class GenresSerializer(serializers.ModelSerializer):
    """
    Movies serializer
    """

    class Meta:
        model = Genres
        fields = ('genre', )
