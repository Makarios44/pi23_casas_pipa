from django.shortcuts import render, redirect
from .models import Casa
from .forms import CasaForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    casas = Casa.objects.all()
    contexto = { 
        'todas_casas': casas  

    }

    return render (request, "index.html", contexto)



def login(request):
        if request.method =="GET":
          return render(request, 'login.html')
        else:
            username = request.POST.get('username')
            password = request.POST.get('senha')   

            user = authenticate(request, username=username, password=password)
            
            if user:
                   return redirect('perfil')
            else:
                   return HttpResponse('email ou senha inválidos')
            


def cadastro(request):
   if request.method == "GET":

      return render (request, "cadastro.html")
   
   else:  
       username = request.POST.get('username')
       email =   request.POST.get('email')
       senha =  request.POST.get('password')
       
       user = User.objects.filter(username=username).first()

       if user:
           return HttpResponse('já existe um usuario com esse username')
       
       user = User.objects.create_user(username=username, email=email, password=senha)
       user.save() 
       return HttpResponse('usuario cadastrado com sucessoo')


def booking(request):
    return render (request, "booking.html")


def formcad(request):   

    form = CasaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    contexto={
        'form_casa':form
    }
    return render (request, "formcad.html", contexto)

def editar_casas(request, id):
    casa = Casa.objects.get(pk=id)
    form = CasaForm(request.POST or None, instance=casa)
    if form.is_valid():
        form.save()
        return redirect('home')
    contexto ={
        'form_casa':form
    }

    return render(request, 'formcad.html', contexto)

def remover_casa(request,id):
    casa = Casa.objects.get(pk=id)
    casa.delete()
    return redirect('home')




def perfil(request):
    return render (request, "perfil.html")
