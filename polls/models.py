import datetime
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# from rest_framework import serializers

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = {'url', 'name', 'email'}


# Our model (table) lar has:
# ID - id do lar
# name - nome do lar
# owner - é uma foreign key para User, ou seja, é apenas um User que é associado a este lar como owner
# users - uma lista de utilizadores, com permissões a definir dentro do Django
class Lar(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='owner', on_delete=CASCADE)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

# O modelo Produto contem:
# ID
# name - nome do produto
# price - preço do produto
# quantity - quantidade deste produto que existe em stock
class Produto(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.name

# O modelo Equipa contem:
# ID
# name - nome desta equipa
# team_user - lista de utilizadores de uma equipa (membros desta)
class Equipa(models.Model):
    name = models.CharField(max_length=30)
    team_user = models.ManyToManyField(User)
    def __str__(self):
        return self.name

# O modelo de Visitas contem:
# ID 
# visit_team - O ForeignKey com Equipa, identifica a equipa responsável pela visita 
# visit_date - data da realização da visita
# description - uma breve descrição da visita
# lar - identifica um único lar visitado com o ForeignKey
# product - lista de produtos utilizados numa visita
# infected_users - lista de utilizadores dados como infetados numa visita
class Visita(models.Model):
    visit_team = models.ForeignKey(Equipa, on_delete=CASCADE)
    visit_date = models.DateField(null=False, blank=False)
    description = models.TextField(default='')
    lar = models.ForeignKey(Lar, on_delete=CASCADE)
    product = models.ManyToManyField(Produto)
    infected_users = models.ManyToManyField(User)
    def __strV__(self):
        return self.description




# class Intervention(models.Model):
#     visited_lar = models.ForeignKey(Lar, on_delete=CASCADE)
#     used_product = models.ManyToManyField(Produto)
#     infected_user = models.ManyToManyField(User)
#     def __str__(self):
#         return self.visited_lar
   

