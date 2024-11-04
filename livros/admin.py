from django.contrib import admin
from .models import Livro, Usuario, Emprestimo  # Importe seus modelos

admin.site.register(Livro)
admin.site.register(Usuario)
admin.site.register(Emprestimo)