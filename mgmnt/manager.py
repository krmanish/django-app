from django.db import models

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
            kwargs['genre__iexact'] = kwargs['genre'].strip()
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
            kwargs['full_name__iexact'] = kwargs['full_name'].strip()
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
            kwargs['name__iexact'] = kwargs['name'].strip()
            del kwargs['name']
        return super(MoviesManager, self).get(*args, **kwargs)
