from django.shortcuts import render, redirect, get_object_or_404
from .models import Casa
from .forms import CasaForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .models import Reserva
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
# Create your views here.

def home(request):
    casas = Casa.objects.all()

    context = { 
        'todas_casas': casas,
    }
    return render(request, "index.html", context=context)

def login_view(request):
    if request.method == "GET":
        return render(request, 'registration/login.html')
    else:
        cpf = request.POST.get('username')  
        password = request.POST.get('senha')   

        user = authenticate(request, username=cpf, password=password)
        
        if user is not None:
            login(request, user)        
        
            return redirect('perfil')
        else:
           
            return redirect('login')

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    else:  
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        cpf = request.POST.get('cpf')
        user_type = request.POST.get('user_type')

        user = User.objects.filter(username=cpf).first()

        if user:
            return HttpResponse('Já existe um usuário com esse CPF')
       
        user = User.objects.create_user(username=cpf, email=email, password=senha)
        user.save() 

        # Adiciona o usuário ao grupo correspondente
        if user_type == 'owner':
            assign_role(user, 'proprietario')
        elif user_type == 'renter':
            assign_role(user, 'locatario')

        # Aplica o decorador de permissão ao usuário, dependendo do tipo
        if user_type == 'owner':
            user_permissions = ['cadastrar_casas', 'excluir_casas', 'editar_casas']
        elif user_type == 'renter':
            user_permissions = ['cadastrar_casas', 'fazer_reservas', 'cancelar_reservas']

        # Aqui você deve aplicar as permissões ao usuário
        for permission in user_permissions:
            user.has_perm(permission)  # Isso cria a permissão no banco de dados para o usuário

        if user:
            login(request, user)
            return redirect('perfil')

        


    return render(request, "cadastro.html")
        
@login_required(login_url='login')

def booking(request):
    casas_disponiveis = Casa.objects.filter(
        reserva__isnull=True
    ).distinct()

    print("Casas Disponíveis:", casas_disponiveis)

    return render(request, "booking.html", {'casas_disponiveis': casas_disponiveis})
# ---------------CRUD CASAS-----------------------#
@login_required
@has_role_decorator('proprietario')
# Exemplo de como salvar uma casa no seu formulário de criação
def formcad(request):
    form = CasaForm()
    if request.method == 'POST': 
        form = CasaForm(request.POST, request.FILES)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            qq = form.cleaned_data['quantidade_quartos']
            pp = form.cleaned_data['possui_piscina']
            ic = form.cleaned_data['introducao_casa']
            fotos = form.files["fotos"]
            preco = form.cleaned_data['preco']
            owner = request.user.id

            Casa.objects.create(nome=nome, quantidade_quartos=qq, possui_piscina=pp, introducao_casa=ic, fotos=fotos, preco=preco, owner_id=owner)

            return redirect('home')
        else:
            return HttpResponse(form.cleaned_data['nome'])
    elif request.method == 'GET':
        context = {
            'form': form,
        }

        return render(request, "formcad.html", context=context)

@login_required
@has_role_decorator('proprietario')
def editar_casas(request, id):
    casa = get_object_or_404(Casa, pk=id)

    # Verifica se o usuário logado é o proprietário da casa
    if request.user == casa.owner:
        form = CasaForm(request.POST or None, instance=casa)
        
        if form.is_valid():
            form.save()
            return redirect('perfil')

        contexto = {
            'form_casa': form
        }
        return render(request, 'formcad.html', contexto)
    else:
        # Adicione aqui o código para lidar com o caso em que o usuário não é o proprietário da casa
        return HttpResponse('Você não tem permissão para editar esta casa.')

@login_required
@has_role_decorator('proprietario')
def remover_casa(request, id):
    # Obtém a instância da casa ou retorna um erro 404 se não existir
    casa = get_object_or_404(Casa, pk=id)

    # Verifica se o usuário logado é o proprietário da casa
    if request.user == casa.owner:
        casa.delete()
        return redirect('home')
    else:
        # Se o usuário não for o proprietário, você pode lidar com isso da maneira desejada,
        # como redirecioná-lo para uma página de erro ou exibir uma mensagem adequada.
        return HttpResponse('Você não tem permissão para excluir esta casa.')
# ------------------END_CRUD_CASAS----------------------#

def views_perfil(request):
    # Recupera todas as casas do banco de dados
    todas_casas = Casa.objects.all()

    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Se estiver autenticado, recupera as casas associadas ao usuário logado
        casas_do_usuario = Casa.objects.filter(owner=request.user)

        # Recupera as reservas associadas ao usuário logado considerando as casas associadas a esse usuário
        reservas_do_usuario = Reserva.objects.filter(casa__in=casas_do_usuario)

        # Renderiza a página de perfil com todas as casas, casas do usuário e reservas do usuário
        return render(request, "perfil.html", {'todas_casas': todas_casas, 'casas_do_usuario': casas_do_usuario, 'reservas_do_usuario': reservas_do_usuario})
    else:
        # Se o usuário não estiver autenticado, renderiza a página de perfil apenas com todas as casas
        return render(request, "perfil.html", {'todas_casas': todas_casas})

   

def is_casa_disponivel(casa_id, check_in_date, check_out_date):
    # Lógica para verificar a disponibilidade da casa para as datas escolhidas
    # (pode depender da estrutura do seu modelo e lógica de reserva)
    reservas = Reserva.objects.filter(casa_id=casa_id, data_check_out__gte=check_in_date, data_check_in__lte=check_out_date)
    return not reservas.exists()

def realizar_reserva(casa_id, check_in_date, check_out_date):
    # Lógica para realizar a reserva
    # (pode depender da estrutura do seu modelo e lógica de reserva)
    Reserva.objects.create(casa_id=casa_id, data_check_in=check_in_date, data_check_out=check_out_date)


def reservar_casa(request):
    if request.method == 'POST':
        casa_id = request.POST.get('casa_id')
        check_in_date = datetime.strptime(request.POST.get('check_in'), "%Y-%m-%d").date()
        check_out_date = datetime.strptime(request.POST.get('check_out'), "%Y-%m-%d").date()

        # Lógica para verificar a disponibilidade e realizar a reserva
        if is_casa_disponivel(casa_id, check_in_date, check_out_date):
           realizar_reserva(casa_id, check_in_date, check_out_date)
        else:
            messages.error(request)
    return redirect ('home')

def cancelar_reserva(request, id):
    # Lógica para cancelar a reserva
    reserva = get_object_or_404(Reserva, id=id)

    # Adicione a lógica específica para cancelar a reserva, por exemplo, deletando-a do banco de dados
    reserva.delete()

    # Adicione uma resposta adequada após o cancelamento
    return HttpResponse("Reserva cancelada com sucesso!")

def criar_casa(request):
    if request.method == 'POST':
        # Processar os dados do formulário
        # ...

        # Criar uma nova casa
        nova_casa = Casa.objects.create(nome="Nome da Casa", quantidade_quartos=3, possui_piscina=True, introducao_casa="Descrição da casa", owner=request.user)

        # Redirecionar para alguma página
        return redirect('alguma_pagina')

    return render(request, 'template_formulario_casa.html')