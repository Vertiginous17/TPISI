from django.contrib import admin

from .models import Equipa, Lar, Produto, Visita

admin.site.register(Equipa)
admin.site.register(Lar)
admin.site.register(Produto)
admin.site.register(Visita)

admin.site.site_header  =  "Visitas aos Lares"  
admin.site.site_title  =  "Visitas aos Lares"
admin.site.index_title  =  "Hello, my dear" 

