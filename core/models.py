from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user( email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser= True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username=None
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=60, unique=True)
    phone_number=models.CharField(max_length=10,validators=[RegexValidator(regex='^[0-9]+$')])
    birth_date=models.DateField(default=None,null=True)
    profile_image=models.ImageField(null=True,blank=True)
    city=models.CharField(max_length=10)
    address=models.CharField(max_length=60)
    postal_code=models.CharField(max_length=5,validators=[RegexValidator(regex='^[0-9]+$')])
    is_student=models.BooleanField(default=False)
    is_member_club=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined=models.DateField(default=timezone.now())
    member_club_reduction= models.FloatField(default=0)

    objects= CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name','city','address','postal_code',]

    def __str__(self) :
        return  self.email
    
    # def has_perms(self,perm,obj=None):
    #     return True
    
    # def has_perm(self,perm,obj=None):
    #     return self.is_admin
    
    # def has_module_perms(self,app_label):
    #     return True
    
    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"
    






