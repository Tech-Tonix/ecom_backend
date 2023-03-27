from .models import CustomUser
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from ecom_backend import settings


class CustomRegisterSerializer(serializers.Serializer):
    username= serializers.CharField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    email= serializers.EmailField(required=True)
    password1= serializers.CharField(write_only=True, required=True)
    password2= serializers.CharField(write_only=True, required=True)
    first_name= serializers.CharField(required=False, write_only=True)
    last_name= serializers.CharField(required=False, write_only=True)
    phone_number=serializers.CharField(required=True)
    birth_date= serializers.DateField(required=True)
    city=serializers.CharField(max_length=10)
    address=serializers.CharField(max_length=60)
    postal_code=serializers.CharField(max_length=5)
    is_student=serializers.BooleanField(default=False)
    is_member_club=serializers.BooleanField(default=False)


    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return{
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'city':self.validated_data.get('city', ''),
            'address':self.validated_data.get('address', ''),
            'postal_code':self.validated_data.get('postal_code', ''),
            'is_student':self.validated_data.get('is_student', ''),
            'is_member_club':self.validated_data.get('is_member_club', '')
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        # self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        fields = ('username', 'email')
        read_only_fields=('email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','birth_date','phone_number','address']