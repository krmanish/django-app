import ast

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from mgmnt.models import Movies


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
                data['user'] = user
                Movies.objects.save_with_related(data)
