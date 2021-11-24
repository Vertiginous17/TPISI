import datetime
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CommaSeparatedIntegerField

class Lar(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='owner', on_delete=CASCADE)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Produto(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Equipa(models.Model):
    name = models.CharField(max_length=30)
    team_user = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Visita(models.Model):
    visit_team = models.ForeignKey(Equipa, on_delete=CASCADE)
    visit_date = models.DateField(null=False, blank=False)
    description = models.TextField(default='')
    lar = models.ForeignKey(Lar, on_delete=CASCADE)
    product = models.ManyToManyField(Produto)
    
    def __str__(self):
        return self.description
   

