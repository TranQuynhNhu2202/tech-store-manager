# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class OrderDetails(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'order_details'


class Orders(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    customer_name = models.CharField(max_length=150)
    customer_email = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=0)
    stock = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
