from django.shortcuts import render, redirect, get_object_or_404
from .models import Casa
from .forms import CasaForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator 


from django.shortcuts import render, redirect, HttpResponse
# Create your views here.

def home(request):
    casas = Casa.objects.all()
    contexto = { 
        'todas_casas': casas  

    }

    return render (request, "index.html", contexto)



def login_view(request):
    if request.method =="GET":
        return render(request, 'registration/login.html')
    else:
        cpf = request.POST.get('username')  
        password = request.POST.get('senha')   

        user = authenticate(request, username=cpf, password=password)
        
        if user is not None:
                login(request, user)        
                return redirect('perfil')
        else:
                return HttpResponse('email ou senha inválidos')
            



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
            user_permissions = ['fazer_reservas', 'cancelar_reservas']

        # Aqui você deve aplicar as permissões ao usuário
        for permission in user_permissions:
            user.has_perm(permission)  # Isso cria a permissão no banco de dados para o usuário

        return HttpResponse('Usuário cadastrado com sucesso')


def booking(request):
    return render (request, "booking.html")

#---------------CRUD CASAS-----------------------#
@login_required
@has_role_decorator('proprietario')
# Exemplo de como salvar uma casa no seu formulário de criação
def formcad(request):
    print("Iniciando formcad")
    try:
        form = CasaForm(request.POST)
        print("Formulário criado")
        if form.is_valid():
            casa = form.save(commit=False)
            casa.owner = request.user  # Define o proprietário como o usuário autenticado
            casa.save()
            print("Casa salva com sucesso")
            return redirect('perfil')
    except Exception as e:
        print(f"Erro ao salvar casa: {e}")

    contexto = {
        'form_casa': form
    }
    return render(request, "formcad.html", contexto)

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
def remover_casa(request,id):
   
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
#------------------END_CRUD_CASAS----------------------#


def views_perfil(request):
  # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Recupera as casas associadas ao usuário logado
        casas_do_usuario = Casa.objects.filter(owner=request.user)

        # Renderiza a página de perfil com as casas do usuário
        return render(request, "perfil.html", {'casas_do_usuario': casas_do_usuario})
    else:
        # Se o usuário não estiver autenticado, redirecione para a página de login
        return redirect('login')