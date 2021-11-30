from os import name
from typing import List
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.fields import EmailField
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm

# from django.http import Http404

from polls.models import Lar, Equipa, Visita, Produto, User

# Root View
def index(request):
    # Checks if user is authenticated, if not, redirects us to the login func
    if not request.user.is_authenticated:
        return render(request, "polls/login.html")

    # Receive all the objects inside a team
    equipas = Equipa.objects.all()
    
    # we create out dictionary, initially empty. we fill it with info from our teams
    context = {
        'index_list' : []
    }

    # Colocamos a lista de equipas
    # teams have name and a bunch of users
    # each user has id, username, name, email, and if it's staff
    for equipa in equipas: 
        index_json = {
            'name' : equipa.name,
            'users' : [{'id': u.id, 'username': u.username, 'name': u.first_name + ' ' + u.last_name, 
                        'email': u.email, 'is_staff': u.is_staff } for u in equipa.team_user.all()]
        }
        context['index_list'].append(index_json)
    
    # renders us to the  index page
    return render(request, 'polls/index.html')

# Metodo para registar um utilizador
def register_request(request):
    # utilizamos o metodo POST para este registo
    if request.method == "POST":
        # Criamos um user form com o metodo que utilizamos anteriormente
	    form = NewUserForm(request.POST)
        # Se este form for valido, guardamos o mesmo e damos login no user
        # dando a mensagem de que o registo foi feito com sucesso
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    return redirect("/equipas/index_equipa.html")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="polls/register.html", context={"register_form":form})


# Metodo para logar um utilizador
def login_request(request):
    # verificamos o metodo para nos certificarmos que é POST 
    # caso nao seja, erro
    if request.user.is_authenticated:
        return render(request, "info/index_info.html")
    if request.method == "POST":
        # inicializamos um form com o nosso request e a nossa data, sendo esta data a info do user
        form = AuthenticationForm(request, data=request.POST)
        # se este form for válido
        if form.is_valid():
        	username = form.cleaned_data.get('username')
        	password = form.cleaned_data.get('password')
        	user = authenticate(username=username, password=password)
        	if user is not None:
        		login(request, user)
        		messages.info(request, f"You are now logged in as {username}.")
        		return redirect("/info/index_info.html")
        	else:
        		messages.error(request,"Invalid username or password.")
        else:
        	messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="polls/login.html", context={"login_form":form})



# Lar view
def index_lares(request):
    #if not request.user.is_authenticated:
    #    return redirect("/admin")

    lar_list = Lar.objects.all()
    #template = loader.get_template('polls/index_lares.html')
    context = {
        'lar_list' : []
    }

    for lar in lar_list:
        lar_json = {
            'id' : lar.id,
            'name' : lar.name,
            'owner' : lar.owner,
            'users' : [{'id': u.id, 'username': u.username, 'name': u.first_name + ' ' + u.last_name, 
                        'email': u.email, 'is_staff': u.is_staff } for u in lar.users.all()]
        }
        context['lar_list'].append(lar_json)

    # return HttpResponse(template.render(context, request))
    return render(request, 'lares/index_lares.html', context)

# Equipa view
def index_equipa(request):
    equipa_list = Equipa.objects.all()
    # name = Equipa.objects.name

    context = {
        'equipa_list' : []
    }
    for equipa in equipa_list:
        equipa_json = {
            'id': equipa.id,
            'name': equipa.name,
            'users': [{'id': u.id, 'username': u.username, 'name': u.first_name + ' ' + u.last_name, 
                        'email': u.email, 'is_staff': u.is_staff } for u in equipa.team_user.all()]
        }
    context['equipa_list'].append(equipa_json)

    return render(request, 'equipas/index_equipa.html', context)

def index_visit(request):
    visit_list = Visita.objects.all()

    number_infected = 0

    context = {
        'visit_list' : []
    }

    for visit in visit_list:
        for u in visit.infected_users.all():
            number_infected+=1

        visit_json = {
            'id' : visit.id,
            'visit_team' : visit.visit_team,
            'visit_date' : visit.visit_date,
            'description' : visit.description,
            'lar' : visit.lar,
            'product' : [{'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in visit.product.all()],
            'infected_users' : number_infected,
        }

        context['visit_list'].append(visit_json)

    return render(request, 'visitas/index_visit.html', context)

def count_infected_user(user):
    return Post.objects.filter(author=user).count()

#Product view
def index_produto(request):
    product_list = Produto.objects.all()
    context = {
        'product_list' : []
    }

    for product in product_list:
        product_json = {
            'name' : product.name,
            'price' : product.price,
            'quantity' : product.quantity,
        }
        context['product_list'].append(product_json)

    return render(request, 'produtos/index_produto.html', context)


# def login_view(request):
   

#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return render(request, 'equipas/index_equipas.html')
#     else:
#         return HttpResponse('You got an error loggin in')
#         #return render(request, 'polls/index_lares.html')

def index_info(request):
    return render(request, 'info/index_info.html')
