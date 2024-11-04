from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView  # Adicione TemplateView aqui
from .models import Livro, Usuario, Emprestimo

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages


class SolicitarEmprestimoView(CreateView):
    model = Emprestimo
    fields = ['livro', 'usuario', 'data_prevista_devolucao']
    template_name = 'livros/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    def form_valid(self, form):
        livro = get_object_or_404(Livro, pk=self.request.POST.get('livro'))
        
        # Verifica se o livro está disponível
        if livro.disponivel:
            form.instance.usuario = self.request.user  # Define o usuário atual
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Desculpe, este livro não está disponível para empréstimo.')
            return self.form_invalid(form)


class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'livros/emprestimo_list.html'

    def get_queryset(self):
        # Filtra os empréstimos para incluir apenas aqueles com livros disponíveis
        return Emprestimo.objects.filter(livro__disponivel=True)

# Função de registro de usuário
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash a senha
            user.save()
            login(request, user)  # Loga o usuário após o registro
            return redirect('index')  # Redireciona para a página inicial
    else:
        form = UserRegistrationForm()
    
    return render(request, 'livros/register.html', {'form': form})

# View personalizada de login
class Index(TemplateView):
    template_name = 'livros/index.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Loga o usuário
            return redirect('index')  # Redireciona para a página inicial
        else:
            return render(request, self.template_name, {'error': 'Credenciais inválidas'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = self.request.user.is_authenticated
        context['usuario_tipo'] = getattr(self.request.user, 'usuario', None)
        return context
# Continue com o resto do seu código...

# Views para Emprestimo
class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'livros/emprestimo_list.html'

class EmprestimoCreateView(CreateView):
    model = Emprestimo
    fields = ['livro', 'usuario', 'data_prevista_devolucao']
    template_name = 'livros/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

class EmprestimoUpdateView(UpdateView):
    model = Emprestimo
    fields = ['livro', 'usuario', 'data_prevista_devolucao', 'data_devolucao', 'renovacoes']
    template_name = 'livros/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

class EmprestimoDeleteView(DeleteView):
    model = Emprestimo
    template_name = 'livros/emprestimo_confirm_delete.html'
    success_url = reverse_lazy('emprestimo_list')

# Views para Livro
class LivroListView(ListView):
    model = Livro
    template_name = 'livros/livro_list.html'

class LivroCreateView(CreateView):
    model = Livro
    fields = ['titulo', 'autor', 'disponivel']
    template_name = 'livros/livro_form.html'
    success_url = reverse_lazy('livro_list')

class LivroUpdateView(UpdateView):
    model = Livro
    fields = ['titulo', 'autor', 'disponivel']
    template_name = 'livros/livro_form.html'
    success_url = reverse_lazy('livro_list')

class LivroDeleteView(DeleteView):
    model = Livro
    template_name = 'livros/livro_confirm_delete.html'
    success_url = reverse_lazy('livro_list')

# Views para Usuario
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'livros/usuario_list.html'

class UsuarioCreateView(CreateView):
    model = Usuario
    fields = ['nome', 'tipo']
    template_name = 'livros/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioUpdateView(UpdateView):
    model = Usuario
    fields = ['nome', 'tipo']
    template_name = 'livros/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'livros/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

# views.py
from django.contrib.auth.models import Group

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Atribuir ao grupo de usuários comuns
            user_group, _ = Group.objects.get_or_create(name='Usuários')
            user.groups.add(user_group)
            # ... resto do código de registro
# views.py
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.groups.filter(name='Administradores').exists())

# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages

# Função para verificar se é administrador
def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.groups.filter(name='Administradores').exists())

# Função para verificar se é usuário comum
def is_common_user(user):
    return user.is_authenticated and user.groups.filter(name='Usuários').exists()

# Views para administradores
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(is_admin, login_url='login')
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@user_passes_test(is_admin, login_url='login')
def manage_books(request):
    books = Livro.objects.all()
    return render(request, 'manage_books.html', {'books': books})

# Views para usuários comuns
@user_passes_test(is_common_user, login_url='login')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@user_passes_test(is_common_user, login_url='login')
def borrow_book(request):
    if request.method == 'POST':
        # Lógica para empréstimo de livro
        pass
    
    # Filtra os livros que estão disponíveis para empréstimo
    books = Livro.objects.filter(disponivel=True)  # Ajuste o campo conforme sua implementação
    return render(request, 'borrow_book.html', {'books': books})

@user_passes_test(is_common_user, login_url='login')
def my_borrowed_books(request):
    borrowed_books = Livro.objects.filter(borrower=request.user)
    return render(request, 'my_borrowed_books.html', {'borrowed_books': borrowed_books})

# View geral para redirecionamento com base no tipo de usuário
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_common_user(request.user):
        return redirect('user_dashboard')
    else:
        messages.error(request, 'Você não tem permissão para acessar o sistema.')
        return redirect('login')



class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_admin or self.request.user.groups.filter(name='Administradores').exists())


