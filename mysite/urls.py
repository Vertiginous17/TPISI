from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

# URLConf
urlpatterns = [
    # /lar/
    # Tudo o que começa por /lar/ é referenciado pelo polls.urls
    path('', include('polls.urls')),
    # /admin/
    path('admin/', admin.site.urls),
]
