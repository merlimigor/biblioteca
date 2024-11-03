from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView  # Adicione TemplateView aqui
from .models import Livro, Usuario, Emprestimo

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

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
