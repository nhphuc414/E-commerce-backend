from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    email = models.CharField(max_length=100, unique=True)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Store(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=False)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_query_name='products')
    image = CloudinaryField('image', null=True)

    class Meta:
        unique_together = ('name', 'store')


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, through='OrderDetail')


class OrderDetail(BaseModel):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'comment')
