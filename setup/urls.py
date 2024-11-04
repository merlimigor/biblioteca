"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from livros.views import register, Index
from django.contrib.auth import views as auth_views
from livros.views import (
    EmprestimoListView, EmprestimoCreateView, EmprestimoUpdateView, EmprestimoDeleteView,
    LivroListView, LivroCreateView, LivroUpdateView, LivroDeleteView,
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView
)

urlpatterns = [
    


    path('', Index.as_view(), name='index'),  # Mapeando a URL raiz
    path('register/', register, name='register'),  # Registro de usuário
    # Adicione outras URLs aqui...
    path('', TemplateView.as_view(template_name='livros/index.html'), name='index'),# Página inicial
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Adiciona a view de login

    path('admin/', admin.site.urls),
    path('', include('livros.urls')),


    # URLs para Emprestimo
    path('emprestimos/', EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/create/', EmprestimoCreateView.as_view(), name='emprestimo_create'),
    path('emprestimos/update/<int:pk>/', EmprestimoUpdateView.as_view(), name='emprestimo_update'),
    path('emprestimos/delete/<int:pk>/', EmprestimoDeleteView.as_view(), name='emprestimo_delete'),

    # URLs para Livro
    path('livros/', LivroListView.as_view(), name='livro_list'),
    path('livros/create/', LivroCreateView.as_view(), name='livro_create'),
    path('livros/update/<int:pk>/', LivroUpdateView.as_view(), name='livro_update'),
    path('livros/delete/<int:pk>/', LivroDeleteView.as_view(), name='livro_delete'),

    # URLs para Usuario
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/create/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/update/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/delete/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    #adm

    
]




