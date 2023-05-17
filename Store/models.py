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



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4) 
    #uuid4 is and identifier we use it to make a complicated id so the users carts are more secure because the don't need to login to make them
    created_at = models.DateTimeField(auto_now_add=True)




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']] # so when the user add the same item 2 times only the quantity becomes 2
