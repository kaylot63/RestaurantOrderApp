from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.BooleanField(default=True)
    category = models.CharField(max_length=50)


class CartItem(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"


class TableCart(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"Cart for Table {self.table_number}"


class Order(models.Model):
    table_number = models.IntegerField()
    items = models.ManyToManyField('Menu', through='OrderedItem')

    def __str__(self):
        return f"Order for Table {self.table_number}"

class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('Menu', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"