from django.urls import path
from .views import (
    Index,
    EmprestimoListView,
    EmprestimoCreateView,
    EmprestimoUpdateView,
    EmprestimoDeleteView,
    LivroListView,
    LivroCreateView,
    LivroUpdateView,
    LivroDeleteView,
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
)

app_name = 'livros'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    
    # Empréstimos
    path('emprestimos/', EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/novo/', EmprestimoCreateView.as_view(), name='emprestimo_create'),
    path('emprestimos/<int:pk>/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_update'),
    path('emprestimos/<int:pk>/deletar/', EmprestimoDeleteView.as_view(), name='emprestimo_delete'),

    # Livros
    path('livros/', LivroListView.as_view(), name='livro_list'),
    path('livros/novo/', LivroCreateView.as_view(), name='livro_create'),
    path('livros/<int:pk>/editar/', LivroUpdateView.as_view(), name='livro_update'),
    path('livros/<int:pk>/deletar/', LivroDeleteView.as_view(), name='livro_delete'),

    # Usuários
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/novo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/deletar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]