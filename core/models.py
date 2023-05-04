from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("the given email is not valid")
        
        user = self.model(
            email=self.normalize_email(email),
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            password=password,
            email=self.normalize_email(email),    
        )

        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser):
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
    date_joined=models.DateField(default=timezone.now())
    # credit_card_info=

    objects= CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    def __str__(self) :
        return  self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()




class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    Category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name



class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)




