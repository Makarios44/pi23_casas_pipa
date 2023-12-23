from django.shortcuts import render, redirect
from .models import Casa
from .forms import CasaForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
# Create your views here.

def home(request):
    casas = Casa.objects.all()
    contexto = { 
        'todas_casas': casas  

    }

    return render (request, "index.html", contexto)

def login(request):
    if request.method == 'POST':
        # Se o formulário foi enviado, processar os dados do formulário
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Se os dados do formulário são válidos, efetuar o login
            auth_login(request, form.get_user())
            return redirect('pagina_inicial')  # Redirecionar para a página inicial após o login
    else:
        # Se o formulário não foi enviado, exibir o formulário de login
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
   
def cadastro(request):
    return render (request, "cadastro.html")





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