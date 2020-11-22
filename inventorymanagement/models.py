from django.db import models
from django.db.models.base import Model

from authentication.models import User

class InventoryItem(models.Model):

    class Units(models.TextChoices):
        NIL = 'nil', ('-')
        GM = 'gm', ('gm')
        KG = 'kg', ('Kg')
        ML = 'ml', ('ml')
        L = 'l', ('l')

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=3, choices=Units.choices, default=Units.NIL)

    def __str__(self) -> str:
        return self.name
