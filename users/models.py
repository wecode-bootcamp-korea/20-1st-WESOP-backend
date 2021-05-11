from django.db       import models

from products.models import Product, ProductSelection

class User(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    create_date  = models.DateTimeField(auto_now_add=True)
    update_date  = models.DateTimeField(auto_now=True)
    skin_type = models.ForeignKey("SkinType", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'users'

class SkinType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'skin_types'
    
class WishList(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    class Meta:
        db_table = 'wish_lists'

class OrderList(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product_selection = models.ForeignKey("products.ProductSelection", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_lists'

class Order(models.Model):
    user =  models.ForeignKey("User", on_delete=models.CASCADE)
    status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    memo = models.TextField(blank=True)
    payment_method = models.ForeignKey("PaymentMethod", on_delete=models.CASCADE, null=True)
    purchased_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    free_delivery = models.BooleanField()

    class Meta:
        db_table = 'orders'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'payment_methods'

    
class OrderStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'order_status'






