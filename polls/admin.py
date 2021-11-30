from django.contrib import admin
from .models import Equipa, Lar, Produto, Visita

@admin.register(Lar)
class LarAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('visit_team', 'visit_date', 'lar')

admin.site.register(Equipa)

admin.site.site_header  =  "Visitas aos Lares"  
admin.site.site_title  =  "Visitas aos Lares"
admin.site.index_title  =  "Lar Management" 
