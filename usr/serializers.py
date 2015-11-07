from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Movies serializer
    """
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, req_data):
        """
        Validate is password and confirm are the same if not then raise error message
        """
        if req_data['password'] != req_data.pop('confirm_password'):
            raise serializers.ValidationError(_("Error: Mismatched Password!"))
        return req_data

    def create(self, validated_data):
        """
        Creates new user if validation done successfully
        """
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')
        read_only_fields = ['is_staff', 'is_superuser']
        write_only_fields = ('password', 'confirm_password')
