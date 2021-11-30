from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from .models import Equipa, Lar, Produto, Visita

# Register the model Lar in the admin page
@admin.register(Lar)
class LarAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

# Register the model Produto in the admin page
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

# Register the model Visita in the admin page
@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_filter = (
        ('infected_users', RelatedOnlyFieldListFilter),
    )
    admin_order_field = ('id',)
    # list_display = ('visit_team', 'visit_date', 'lar')

# Register the model Equipa in the admin page
# We did this differently cause there's no need of a "special treatment" for our Equipa model
admin.site.register(Equipa)

admin.site.site_header  =  "Visitas aos Lares"  
admin.site.site_title  =  "Visitas aos Lares"
admin.site.index_title  =  "Lar Management" 
