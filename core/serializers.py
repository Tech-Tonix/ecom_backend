from rest_framework import serializers
from .models import CustomUser
from djoser.serializers import (
    UserCreateSerializer as BaseUserSerializer,)


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ( 'email','password' ,'first_name', 'last_name', 'phone_number',
                  'birth_date','city', 'address', 'postal_code',
                  'is_student', 'is_member_club','member_club_reduction')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['first_name','last_name','email','birth_date','phone_number','address','postal_code','member_club_reduction','profile_image']






