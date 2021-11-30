from django.urls import path

from . import views

app_name = 'polls'

# URLConf
urlpatterns = [
    #  root
    path("", views.index, name='index'),

    # /register/
    path("register/", views.register_request, name="register"),
    
    # /login/
    path("login/", views.login_request, name="login"),

    # /lar/
    path("lar/", views.index_lares, name='index_lares'),

    # /equipas/
    path('equipa/', views.index_equipa, name='index_equipa'),

    # /produto/
    path('produto/', views.index_produto, name='index_produto'),

    # /visit/
    path('visit/', views.index_visit, name='index_visit'),

    # /info/
    path('info/', views.index_info, name='index_info.html')
]