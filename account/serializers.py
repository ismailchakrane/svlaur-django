from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','last_name', 'first_name', 'email', 'password','major','year_of_major',
                  'linkedin_link','place_of_work','job_title','year_of_graduate','is_graduate',
                  'is_admin')
        