from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import render, redirect



class Livro(models.Model):
    titulo = models.CharField(max_length=200, null=False, blank=False)
    autor = models.CharField(max_length=100, null=False, blank=False)
    disponivel = models.BooleanField(default=True) 

    def __str__(self):
        return self.titulo


class Usuario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    tipo = models.CharField(max_length=50, choices=[('membro', 'Membro'), ('funcionario', 'Funcionário')], default='membro')

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField(null=False, blank=False)
    data_devolucao = models.DateField(null=True, blank=True)
    renovacoes = models.IntegerField(default=0)  

    def __str__(self):
        return f"{self.usuario} - {self.livro}"
from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = 'livros/index.html'  # Caminho para o template

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Loga o usuário
            return redirect('index')  # Redireciona para a página inicial
        else:
            # Caso o login falhe, você pode retornar uma mensagem de erro
            return render(request, self.template_name, {'error': 'Credenciais inválidas'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user'] = self.request.user.is_authenticated
        context['usuario_tipo'] = getattr(self.request.user, 'usuario', None)
        return context

