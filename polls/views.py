from os import name
from typing import List
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm

# from django.http import Http404

from polls.models import Lar, Equipa, Visita

# Root View
def index(request):
    if not request.user.is_authenticated:
        return render(request, "polls/login.html")

    return render(request, 'polls/index.html')

def register_request(request):
    if request.method == "POST":
	    form = NewUserForm(request.POST)
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    return redirect("equipas:index_equipa")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="polls/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
        	username = form.cleaned_data.get('username')
        	password = form.cleaned_data.get('password')
        	user = authenticate(username=username, password=password)
        	if user is not None:
        		login(request, user)
        		messages.info(request, f"You are now logged in as {username}.")
        		return redirect("equipas:index_equipa")
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
    equipa = Equipa.objects.all()
    name = Equipa.objects.name
    
    context = {
        'equipa_list' : equipa,
        'name' : name,
    }
    return render(request, 'equipas/index_equipa.html', context)

def index_visit(request):
    visit_list = Visita.objects.all()
    product = Visita.product

    context = {
        'visit_list' : []
    }

    for visit in visit_list:
        visit_json = {
            'id' : visit.id,
            'visit_team' : visit.visit_team,
            'visit_date' : visit.visit_date,
            'description' : visit.description,
            'lar' : visit.lar,
            'product' : [{'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in visit.product.all()],
        }
        context['visit_list'].append(visit_json)

    return render(request, 'visitas/index_visit.html', context)


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'equipas/index_equipas.html')
    else:
        return HttpResponse('You got an error loggin in')
        #return render(request, 'polls/index_lares.html')


def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/login_error.html')

def results(request, lar_id):
    response = "You're looking at what's inside lar number %s."
    return HttpResponse(response % lar_id)

def detail(request, lar_id):
    lar = get_object_or_404(Lar, pk=lar_id)
    return render(request, 'polls/detail.html', {'lar': lar})
