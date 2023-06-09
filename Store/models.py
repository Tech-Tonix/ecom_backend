from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator
from core.models import CustomUser



# class Promotion(models.Model):
#     description = models.CharField(max_length=255)
#     discount = models.FloatField()




class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    image_urls = models.JSONField(default=list)
    last_update = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='products')
    # promotions = models.ManyToManyField(Promotion, blank=True)
    rating_rv = models.FloatField(default=0)
    rating_nb = models.PositiveIntegerField(default=0)
    # image = models.ImageField(blank=True, null=True,upload_to='product_images/')
    size = models.CharField(max_length=10,null=True, blank=True)
    color = models.CharField(max_length=20,null=True, blank=True)
    discount = models.FloatField()
    def __str__(self) :
        return self.name




# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,)
#     #image = models.ImageField( null=True, blank=True, upload_to = 'product_images/')




class CartItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
          return f"Cart-item ID: {self.id} - Customer: {self.customer.email}"



class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_PACKED = 'A'
    STATUS_SHIPPED = 'S'
    STATUS_DELIVERED = 'D'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PACKED, 'Packed'),
        (STATUS_SHIPPED,'Shipped'),
        (STATUS_DELIVERED, 'Delivered')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_number = models.UUIDField(default=uuid4, editable=False)
    

    def __str__(self):
      return f"Order ID: {self.id} - Customer: {self.customer.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='item')
    quantity = models.PositiveSmallIntegerField()


    def __str__(self):
        return f"Order-item ID: {self.id} - Customer: {self.order.customer.email}"




class ArchivedOrder(models.Model):
    STATUS_PENDING = 'P'
    STATUS_PACKED = 'A'
    STATUS_SHIPPED = 'S'
    STATUS_DELIVERED = 'D'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PACKED, 'Packed'),
        (STATUS_SHIPPED,'Shipped'),
        (STATUS_DELIVERED, 'Delivered')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
      return f"Archived_Order ID: {self.id} - Customer: {self.customer.email}"



class ArchivedOrderItems(models.Model):
    archived_order = models.ForeignKey(ArchivedOrder, on_delete=models.CASCADE,related_name='archived_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='archived_item')
    quantity = models.PositiveSmallIntegerField()


    def __str__(self):
        return f"Archived_Order-item ID: {self.id} - Customer: {self.archived_order.customer.email}"
