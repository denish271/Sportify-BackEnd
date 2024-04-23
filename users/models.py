from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150,null=False,blank=False)
    email = models.CharField(max_length=150,unique=True)
    password = models.CharField(max_length=150,null=False,blank=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Product(models.Model):
    image = models.ImageField(upload_to='uploads/images',null=True)
    name = models.CharField(max_length=150,null=False,blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True)
    category = models.CharField(max_length=30,default='all',null=False,blank=False)
    ratings = models.DecimalField(max_digits=5, decimal_places=2)
    feature = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
# class Order(models.Model):
#     name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
#     amount = models.FloatField(_("Amount"), null=False, blank=False)
#     status = CharField(
#         _("Payment Status"),
#         default=PaymentStatus.PENDING,
#         max_length=254,
#         blank=False,
#         null=False,
#     )
#     provider_order_id = models.CharField(
#         _("Order ID"), max_length=40, null=False, blank=False
#     )
#     payment_id = models.CharField(
#         _("Payment ID"), max_length=36, null=False, blank=False
#     )
#     signature_id = models.CharField(
#         _("Signature ID"), max_length=128, null=False, blank=False
#     )

#     def __str__(self):
#         return f"{self.id}-{self.name}-{self.status}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Address(models.Model):
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    area= models.CharField(max_length=100)
    flat= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} shipping Address {self.country}-{self.state}-{self.city}"

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment of {self.amount} made on {self.payment_date}"  

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField(default=1)
    address = models.ForeignKey(Address,on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"