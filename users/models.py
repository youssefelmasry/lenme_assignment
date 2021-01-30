from django.db import models
from django.contrib.auth.models import AbstractUser

class LenmeUser(AbstractUser):
    user_types = [('investor', 'Investor'), ('borrower', 'Borrower')]

    email = models.EmailField(unique=True, max_length=254)
    usertype = models.CharField(choices=user_types, max_length=20)
    userbalance = models.FloatField(default=0)

    def __str__(self):
        return self.username