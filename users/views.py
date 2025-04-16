from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
# UserCreationForm cria um formulario da biblioteca forms para cadastrar os usuarios
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Faz logout do usuario"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """Faz o cadastro de um novo usuário."""
    # aqui ele ira verificar se o usuario esta authenticado ou seja logado
    # se estiver e caso voce tente acessar a pagina register estando logado ele ira te redirecionar
    # para pagina index
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method != 'POST':
        # exibe o formulário de cadastro em branco
        form = UserCreationForm()
        
    else:
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
        # Faz login do usuário e o redireciona para a página inicial
        # esse authenticate vai la dentro do banco de dados do usuario verificar 
        # se realmente existe e se ele realmente pode ser authenticado
            authenticate_user = authenticate(username = new_user.username, password = request.POST['password1'])
            
            #login serve para ele logar, ele vai receber o usuario e senha
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)