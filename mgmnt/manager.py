from django.db import models


TRIM_SPACES = lambda info: info.strip()


class GenresManager(models.Manager):
    """
    Genre table manager
    """
    def get(self, *args, **kwargs):
        """
        Override filter to compare genre with case insensitive and
        strip spaces around string
        """
        if 'genre' in kwargs:
            kwargs['genre__iexact'] = TRIM_SPACES(kwargs['genre'])
            del kwargs['genre']
        return super(GenresManager, self).get(*args, **kwargs)

    def bulk_get_or_create(self, genre_list):
        """
        Bulk get or create objects
        Note: Bulk create method cant be used as we need to get existing record instead of creating duplicate
        Need to look into how it can be enhanced further to cope up with bulk_create method
        """
        genre_objs = []

        for genre in genre_list:
            genre = genre.strip()
            if genre:
                genre_obj, created = self.get_or_create(genre=genre)
                if created:
                    genre_obj.save()
                genre_objs.append(genre_obj)
        return genre_objs


class DirectorsManager(models.Manager):
    """
    Directors table manager
    """
    def get(self, *args, **kwargs):
        """
        Override filter to compare genre with case insensitive and
        strip spaces around string
        """
        if 'full_name' in kwargs:
            kwargs['full_name__iexact'] = TRIM_SPACES(kwargs['full_name'])
            del kwargs['full_name']
        return super(DirectorsManager, self).get(*args, **kwargs)

    def bulk_get_or_create(self, dir_name_list):
        """
        Bulk get or create objects
        """
        dir_ids = []

        for name in dir_name_list:
            name = name.strip()
            if name:
                dir_obj, created = self.get_or_create(full_name=name)
                if created:
                    dir_obj.save()
                dir_ids.append(dir_obj.id)
        return dir_ids


class MoviesManager(models.Manager):
    """
    Movies table manager
    """

    def get(self, *args, **kwargs):
        """
        Override filter to compare genre with case insensitive and
        strip spaces around string
        """
        if 'name' in kwargs:
            kwargs['name__iexact'] = TRIM_SPACES(kwargs['name'])
            del kwargs['name']
        return super(MoviesManager, self).get(*args, **kwargs)

    def save_with_related(self, data, movie_obj=False):
        """
        Save or update info with all required info
        """

        from mgmnt.models import Directors, Genres

        name = TRIM_SPACES(data['name'])
        genre_list = data['genre']  # Should be a list of name
        director_name = TRIM_SPACES(data['director'])  # Director Name
        imdb_score = data['imdb_score']  # imdb score

        genre_list = [genre_list] if not isinstance(genre_list, list) else genre_list
        genre_list = map(TRIM_SPACES, genre_list)

        # Genre objects
        genre_objs = Genres.objects.bulk_get_or_create(genre_list)

        # Director object
        director, created = Directors.objects.get_or_create(full_name=director_name)
        if created:
            director.save()

        if not movie_obj:
            # Create Movies object
            movie_obj, created = self.model.objects.get_or_create(name=name, director=director)
            if created:
                movie_obj.created_user = data['user']

        movie_obj.imdb_score = imdb_score

        # Delete all all related genre object
        self.model.genre.through.objects.filter(movies=movie_obj).delete()

        for obj in genre_objs:
            movie_obj.genre.add(obj)
        movie_obj.save()
