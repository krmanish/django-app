import django_filters
from mgmnt.models import Directors, Genres, Movies


class IMDBBaseFilter(django_filters.FilterSet):
    """
    IMDB Base class filter
    """
    from_date = django_filters.DateTimeFilter(name='created_ts', lookup_type='gte')


class MoviesFilter(IMDBBaseFilter):
    """
    Create filter criterias

    Search case insensitive movie name, director's name, and genre name
    """

    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    director_name = django_filters.CharFilter(name='director__full_name', lookup_type='icontains')
    genre_name = django_filters.CharFilter(name='genre__genre', lookup_type='icontains')
    # from_year = django_filters.DateTimeFilter(name='created_ts__year', lookup_type='gte')

    # Search with maximum imdb rating 4 i.e <=4
    max_imdb = django_filters.NumberFilter(name='imdb_score', lookup_type='lte')
    # Search with minimum imdb rating 4 i.e >4
    min_imdb = django_filters.NumberFilter(name='imdb_score', lookup_type='gt')

    # Search with popularity 4 i.e <=4
    max_popularity = django_filters.NumberFilter(name='popularity', lookup_type='lte')
    # Search with minimum imdb rating 4 i.e >4
    min_popularity = django_filters.NumberFilter(name='popularity', lookup_type='gt')

    class Meta:
        model = Movies
        fields = ('name', 'imdb_score', 'popularity', 'director_name', 'genre_name',
                  'max_imdb', 'min_imdb', 'max_popularity', 'min_popularity', 'from_date')


class GenresFilter(IMDBBaseFilter):
    """
    Genres Class filter
    """
    genre = django_filters.CharFilter(name='genre', lookup_type='icontains')

    class Meta:
        model = Genres
        fields = ('genre', 'from_date')


class DirectorsFilter(IMDBBaseFilter):
    """
    Directors Class filter
    """
    name = django_filters.CharFilter(name='full_name', lookup_type='icontains')

    class Meta:
        model = Genres
        fields = ('name', 'from_date')
