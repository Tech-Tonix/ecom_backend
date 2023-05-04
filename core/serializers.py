from .models import CustomUser, Category, Product
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from ecom_backend import settings
from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None 
    email= serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    password1= serializers.CharField(write_only=True, required=True)
    password2= serializers.CharField(write_only=True, required=True)
    first_name= serializers.CharField(required=False, write_only=True)
    last_name= serializers.CharField(required=False, write_only=True)
    phone_number=serializers.CharField(required=True,write_only=True)
    birth_date= serializers.DateField(required=True)
    city=serializers.CharField(max_length=10)
    address=serializers.CharField(max_length=60)
    postal_code=serializers.CharField(max_length=5)
    is_student=serializers.BooleanField(default=False)
    is_member_club=serializers.BooleanField(default=False)

    def validate(self, data):
  
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(_("This email address is already in use."))
        return data

    def get_cleaned_data(self):
        """
        Return the cleaned data with email instead of username.
        """
        super().get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'profile_image': self.validated_data.get('profile_image', None),
            'city': self.validated_data.get('city', ''),
            'address': self.validated_data.get('address', ''),
            'postal_code': self.validated_data.get('postal_code', ''),
            'is_student': self.validated_data.get('is_student', False),
            'is_member_club': self.validated_data.get('is_member_club', False)
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone_number = self.cleaned_data.get('phone_number')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.city = self.cleaned_data.get('city')
        user.address = self.cleaned_data.get('address')
        user.postal_code = self.cleaned_data.get('postal_code')
        user.is_student = self.cleaned_data.get('is_student')
        user.is_member_club = self.cleaned_data.get('is_member_club')
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        fields = ('email','phone_number')
        read_only_fields=('email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','birth_date','phone_number','address']




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'inventory',
                  'unit_price', 'Category']

