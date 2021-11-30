from os import name
from typing import List
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.fields import EmailField
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required

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
                        'email': u.email, 'is_staff': u.is_staff } for u in equipa.user.all()]
        }
        context['index_list'].append(index_json)
    
    # renders us to the  index page
    return render(request, 'polls/index.html')

def register_request(request):
    # we use POST for this register
    # we check if the method is POST, if it isn't we raise an error
    if request.method == "POST":
        # we create a form with POST
	    form = NewUserForm(request.POST)
        # if the form is valid, we save it and save a user
        # giving the message that the regist has been done successfuly
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    # we redirect over to equipas
		    return redirect("/info/")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="polls/register.html", context={"register_form":form})


# method to log user in
def login_request(request):
    if request.user.is_authenticated:
        return render(request, "info/index_info.html")
    # we check to be sure the method is POST
    # if not, error
    if request.method == "POST":
        # we start a form with out request and our data, being this one the data of the user
        form = AuthenticationForm(request, data=request.POST)
        # if the form is valid we get the username and the password provided
        if form.is_valid():
        	username = form.cleaned_data.get('username')
        	password = form.cleaned_data.get('password')
        	user = authenticate(username=username, password=password)
        	if user is not None:
        		login(request, user)
        		messages.info(request, f"You are now logged in as {username}.")
        		# return redirect("index_equipa")
        		return redirect("/info/")
        	else:
        		messages.error(request,"Invalid username or password.")
        else:
        	messages.error(request,"Invalid username or password.")
    # we save our form as an AuthenticationForm, and render it
    form = AuthenticationForm()
    return render(request=request, template_name="polls/login.html", context={"login_form":form})



# Lar view
# Requires Login to access info
@login_required(login_url='/login/')
def index_lares(request):
    #if not request.user.is_authenticated:
    #    return redirect("/admin")

    lar_list = Lar.objects.all()
    #template = loader.get_template('polls/index_lares.html')

    # we start our dictionary as empty 
    context = {
        'lar_list' : []
    }
    
    # for each lar, we create a lar_json that has an id, name, owner
    # it also has a list of users, being those the lar users
    for lar in lar_list:
        lar_json = {
            'id' : lar.id,
            'name' : lar.name,
            'owner' : lar.owner,
            'users' : [{'id': u.id, 'username': u.username, 'name': u.first_name + ' ' + u.last_name, 
                        'email': u.email, 'is_staff': u.is_staff } for u in lar.users.all()]
        }
        # 
        context['lar_list'].append(lar_json)

    # return HttpResponse(template.render(context, request))
    return render(request, 'lares/index_lares.html', context)

# Equipa view
# requires login to access equipa
@login_required(login_url='/login/')
def index_equipa(request):
    equipa_list = Equipa.objects.all()
    # name = Equipa.objects.name

    context = {
        'equipa_list' : []
    }
    # for each equipa, we create a equipa_json that has an id, name
    # it also has a list of users, being those the equipa users
    for equipa in equipa_list:
        equipa_json = {
            'equipa_list': equipa_list,
            'id': equipa.id,
            'name': equipa.name,
            'user': [{'id': u.id, 'username': u.username, 'name': u.first_name + ' ' + u.last_name, 
                        'email': u.email, 'is_staff': u.is_staff } for u in equipa.user.all()]
        }
    context['equipa_list'].append(equipa_json)

    return render(request, 'equipas/index_equipa.html', context)

# Visit view
# requires login to access visits
@login_required(login_url='/login/')
def index_visit(request):
    # we create a visit with all the objects inside Visita
    visit_list = Visita.objects.all()
    #  keeps the number of actual infected on all the visits
    total_infected = 0

    context = {
        'visit_list' : []
    }

    for visit in visit_list:
        # This is a variable to help us count the infected users 
        number_infected = 0
        #if there's an user inside all the users inside visit
        # we increment the number of infecteds for a given visit
        for u in visit.infected_users.all():
            number_infected+=1
        # creating our json file for our users
        visit_json = {
            'id' : visit.id,
            'visit_team' : visit.visit_team,
            'visit_date' : visit.visit_date,
            'description' : visit.description,
            'lar' : visit.lar,
            # inserting products inside this variable for each product inside visit
            'product' : [{'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in visit.product.all()],
            'infected_users' : number_infected,
        }
        # we append visit_json to our previous context, or our dictionary
        context['visit_list'].append(visit_json)

    return render(request, 'visitas/index_visit.html', context)

#Product view
@login_required(login_url='/login/')
def index_produto(request):
    product_list = Produto.objects.all()
    context = {
        'product_list' : []
    }
    # for each product inside our list of products, we just pass the name, price and quantity over to the html
    for product in product_list:
        product_json = {
            'name' : product.name,
            'price' : product.price,
            'quantity' : product.quantity,
        }
        context['product_list'].append(product_json)

    return render(request, 'produtos/index_produto.html', context)

def index_info(request):
    return render(request, 'info/index_info.html')

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
