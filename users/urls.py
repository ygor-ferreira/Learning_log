from django.urls import path
# para não dar conflito criar um apelido para as views de 
# autenticação de login
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #aqui esta criando a pagina de login template_name: é apenas a 
    #rota que voce deseja colocar para achar o arquivo login.hmtl
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #fazer o path para logout
    path('logout', views.logout_view, name='logout'),
    #path para registro
    path('register', views.register, name='register')
]
