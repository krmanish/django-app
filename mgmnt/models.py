from django.db import models
from django.contrib.auth.models import User
from .manager import GenresManager, DirectorsManager, MoviesManager


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
        return cls.objects.filter(is_active=True)


    objects = GenresManager()


class Directors(IMDBDatetime):
    """
    All Director list
    """
    full_name = models.CharField(unique=True, max_length=255, help_text="Directors full name")
    is_active = models.BooleanField(default=True, help_text="Flags to mark data as active or inactive")

    def __unicode__(self):
        """
        Return object info
        """
        return self.full_name

    @classmethod
    def get_all(cls):
        """
        Get All active Record
        """
        return cls.objects.filter(is_active=True)

    objects = DirectorsManager()


class Movies(IMDBDatetime):
    """
    Model to manage all movies info
    """
    created_user = models.ForeignKey(User, db_index=True, blank=True, null=True)
    genre = models.ManyToManyField(Genres, db_index=True)
    director = models.ForeignKey(Directors, db_index=True)
    popularity = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="99popularity")
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
    def get_all_movies(self):
        """
        Get all active and non-deleted movies list
        """
        return self.objects.filter(is_active=True, is_deleted=False, director__is_active=True)

    @classmethod
    def get_name_by_genre(self, genre_id):
        """
        Get all movies by genre
        """
        return self.objects.filter(is_active=True, is_deleted=False, genre__id=genre_id)

    @classmethod
    def get_name_by_user(self, user_id):
        """
        get record by user
        """
        return self.objects.filter(is_active=True, is_deleted=False, user__id=user_id)

    @classmethod
    def get_name_by_user(self, director_id):
        """
        get movies by director
        """
        return self.objects.filter(is_active=True, is_deleted=False, director__id=director_id)
