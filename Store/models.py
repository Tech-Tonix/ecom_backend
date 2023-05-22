from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator
from core.models import CustomUser



class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()




class Category(models.Model):
    title = models.CharField(max_length=255)
    # featured_products = models.ManyToManyField(
    #     'Product', null=True, related_name='+', blank=True)

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
    categories = models.ManyToManyField(Category, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    rating_rv = models.FloatField(default=0)
    rating_nb = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True, null=True,upload_to='product_images/')

    def __str__(self) -> str:
        return self.name
    

class CartItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.id)



class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETE = 'C'
    STATUS_FAILED = 'F'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='item')
    quantity = models.PositiveSmallIntegerField()


