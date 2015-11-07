from django.contrib.auth.models import User
from django.db import models

from .manager import DirectorsManager, GenresManager, MoviesManager


class IMDBDatetime(models.Model):
    """
    Abstract model that will be used in all other models
    """
    created_ts = models.DateTimeField(auto_now_add=True, help_text="Created timespan for each record")
    updated_ts = models.DateTimeField(auto_now_add=False, auto_now=True, help_text="Updated timespan for each record")

    class Meta:
        abstract = True


class Genres(IMDBDatetime):
    """
    Model to store all default genre
    """
    genre = models.CharField(max_length=25, unique=True, help_text="Genre Name")
    is_active = models.BooleanField(default=True, help_text="Flags to mark data as active or inactive")

    class Meta:
        unique_together = ('genre', 'is_active')

    def __unicode__(self):
        """
        Return object info
        """
        return self.genre

    @classmethod
    def get_all(cls):
        """
        Get All active Record
        """
        return cls.objects.filter(is_active=True).order_by('-updated_ts')

    objects = GenresManager()


class Directors(IMDBDatetime):
    """
    Model to store all director name
    """
    full_name = models.CharField(unique=True, max_length=255, help_text="Directors full name")
    is_active = models.BooleanField(default=True, help_text="Flags to mark data as active or inactive")

    def __unicode__(self):
        """
        Return object info
        """
        return self.full_name


    class Meta:
        unique_together = ('full_name', 'is_active')

    @classmethod
    def get_all(cls):
        """
        Get All active Record
        """
        return cls.objects.filter(is_active=True).order_by('-updated_ts')

    objects = DirectorsManager()


class Movies(IMDBDatetime):
    """
    Model to manage all movies info
    """
    created_user = models.ForeignKey(User, db_index=True, blank=True, null=True)
    genre = models.ManyToManyField(Genres, db_index=True)
    director = models.ForeignKey(Directors, db_index=True)
    imdb_score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, db_index=True, help_text="IMDB scores")
    name = models.CharField(max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, help_text="Flags to mark data as active or inactive")
    is_deleted = models.BooleanField(default=False, help_text="Delete Flag")

    objects = MoviesManager()

    class Meta:
        unique_together = ('director', 'name', 'is_deleted')

    def __unicode__(self):
        """
        Return object info
        """
        return self.name

    @classmethod
    def get_all_movies(cls):
        """
        Get all active and non-deleted movies list
        """
        return cls.objects.filter(is_active=True, is_deleted=False, director__is_active=True).order_by('-updated_ts')

    @property
    def popularity(self):
        """
        Get 99popularity value
        """
        return self.imdb_score * 10

    @classmethod
    def get_name_by_genre(cls, genre_id):
        """
        Get all movies by genre
        """
        return cls.objects.filter(is_active=True, is_deleted=False, genre__id=genre_id)

    @classmethod
    def is_exist_by_name_director(cls, name, director_name):
        """
        get record by movie name and director name
        """
        return cls.objects.filter(
            name__iexact=name, is_active=True, is_deleted=False,
            director__full_name__iexact=director_name, director__is_active=True)

    @classmethod
    def get_name_by_user(cls, director_id):
        """
        get movies by director
        """
        return cls.objects.filter(is_active=True, is_deleted=False, director__id=director_id)
