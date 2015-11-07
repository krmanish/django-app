from mgmnt.models import Directors, Genres, Movies
from rest_framework import serializers



class DirectorsSerializer(serializers.ModelSerializer):
    """
    Movies serializer
    """

    class Meta:
        model = Directors
        fields = ('id', 'full_name', )


class GenresSerializer(serializers.ModelSerializer):
    """
    Movies serializer
    """

    class Meta:
        model = Genres
        fields = ('id', 'genre', )


class MoviesSerializer(serializers.ModelSerializer):
    """
    Movies serializer for list and retrieve
    """
    director_name = serializers.StringRelatedField(source='director')
    genre_list = serializers.StringRelatedField(source='genre', many=True)

    class Meta:
        model = Movies
        fields = ('id', 'name', 'imdb_score', 'popularity', 'director_name', 'genre_list')


class CreateUpdateMovieSerializer(serializers.Serializer):
    """
    Create/Update Movie Serializer with validations
    """
    director = serializers.CharField(max_length=255, required=True)
    genre = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True)
    )
    name = serializers.CharField(max_length=255, required=True)
    imdb_score = serializers.DecimalField(max_digits=2, decimal_places=1)

    def validate(self, attrs):
        """
        Validate movies request
        :param attrs: dictionary will have all data
        :return: attrs on success else raise Validation error
        """

        # Check this validation for post request
        request = self.context.get('request')
        if request and request.method in ('POST', ):
            name = attrs.get('name', '').strip()
            director = attrs.get('director', '').strip()
            is_exist = Movies.is_exist_by_name_director(name, director)

            if is_exist:
                raise serializers.ValidationError('Error: Movie Name with director exists in our system')

        return attrs
