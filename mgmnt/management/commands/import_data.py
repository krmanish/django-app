import ast
from mgmnt.models import Genres, Directors, Movies
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

class Command(BaseCommand):
    """
    Import Data to db
    """
    file_name = settings.BASE_DIR + '/resources/'+ 'imdb.json'

    def file_data(self):
        """
        Return file content with type
        """
        # Return data of the json object file
        with open(self.file_name, 'r') as f_obj:
            data_obj = f_obj.read()

            # Convert file data to actual object data i.e to list
            return ast.literal_eval(data_obj)


    def handle(self, *args, **kwargs):
        """
        Set file content to different table
        """
        trim_space = lambda info: info.strip()
        data_list = self.file_data()
        user = User.objects.get(id=1)
        for data in data_list:
            if isinstance(data, dict):
                genre_list = data.get('genre', [])

                # Strip spaces around string
                genre_list = map(trim_space, genre_list)
                direct_name = trim_space(data.get('director', ''))
                name = trim_space(data.get('name', ''))

                popularity = data.get('99popularity')
                imdb_score = data.get('imdb_score')

                # Genre objects
                genre_objs = Genres.objects.bulk_get_or_create(genre_list)

                # Director object
                director, created = Directors.objects.get_or_create(full_name=direct_name)
                if created:
                    director.save()

                # Movies object
                movie_obj, created = Movies.objects.get_or_create(name=name, director=director)
                if created:
                    movie_obj.popularity = popularity
                    movie_obj.imdb_score = imdb_score
                    movie_obj.created_user = user
                    for obj in genre_objs:
                        movie_obj.genre.add(obj)
                    movie_obj.save()
