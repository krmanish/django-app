import django_filters
from mgmnt.models import Movies


class MoviesFilter(django_filters.FilterSet):
    """
    Create filter criterias

    Search case insensitive movie name, director's name, and genre name
    """
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    director_name = django_filters.CharFilter(name='director__full_name', lookup_type='icontains')
    genre_name = django_filters.CharFilter(name='genre__genre', lookup_type='icontains')

    class Meta:
        model = Movies
        fields = ('name', 'imdb_score', 'popularity', 'director_name', 'genre_name', )
