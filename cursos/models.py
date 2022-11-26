from django.db import models
from usuarios.models import Usuario
from datetime import datetime

class Cursos(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    thumb = models.ImageField(upload_to = "thumb_cursos")

    def __str__(self) -> str:
        return self.nome

class Aulas(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    aula =  models.CharField(max_length = 255)
    curso = models.ForeignKey(Cursos, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome

class Comentarios(models.Model): # verifica de quem é o comentário
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)
    comentario = models.TextField()
    data = models.DateTimeField(default =  datetime.now) # é salvo em texto a data do comentário
    aula = models.ForeignKey(Aulas, on_delete = models.DO_NOTHING) # em qual aula foi feito o comentário

    def __str__(self) -> str:
        return self.usuario.nome

class NotasAulas(models.Model):
    choices = (
        ('p', 'Péssimo'),
        ('r', 'Ruim'),
        ('re', 'Regular'),
        ('b', 'bom'),
        ('o', 'Ótimo')
    )

    aula = models.ForeignKey(Aulas, on_delete=models.DO_NOTHING)
    nota = models.CharField(max_length=50, choices=choices)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)        