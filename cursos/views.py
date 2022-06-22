from django.shortcuts import HttpResponse
from django.shortcuts import render, resolve_url
from django.shortcuts import redirect
from .models import Aulas, Cursos, Comentarios, NotasAulas
import json

def home(request):
    if request.session.get('usuario'):
        cursos = Cursos.objects.all() #captura todos os cursos do BD
        
        request_usuario = request.session.get('usuario') #captura o id do usuário
        return render(request, 'home.html', {'cursos': cursos, 'request_usuario': request_usuario})#envia p/ p HTML o id e o cursos
    else:
        return redirect('/auth/login/?status=2')

def curso(request, id): #recebe um parâmetro id do curso
    v_curso = Cursos.objects.get(id = id)
    aulas = Aulas.objects.filter(curso = v_curso) # busca todas as aulas do curso escolhido
    return render(request, 'curso.html', {'aulas': aulas})

def aula(request, id):
    if request.session.get('usuario'):
        aula = Aulas.objects.get(id = id)
        usuario_id = request.session['usuario']
        comentarios = Comentarios.objects.filter(aula = aula).order_by('-data')

        request_usuario = request.session.get('usuario')
        usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request_usuario) #verifica se usuário já avaliou
        avaliacoes = NotasAulas.objects.filter(aula_id = id) #exibe todas as avaliações

        return render(request, 'aula.html', {'aula': aula,
                                            'usuario_id': usuario_id,
                                            'comentarios': comentarios,
                                            'request_usuario': request_usuario,
                                            'usuario_avaliou': usuario_avaliou,
                                            'avaliacoes': avaliacoes})
    else:
        return redirect('/auth/login/?status=2')

def comentarios(request): # recebe os dados vindos do comentário
    usuario_id = int(request.POST.get('usuario_id')) # qual
    comentario = request.POST.get('comentario') # quem 
    aula_id = int(request.POST.get('aula_id')) # qual

    comentario_instancia = Comentarios(usuario_id = usuario_id, # pega o comentário 
                                       comentario = comentario,
                                       aula_id = aula_id)
    comentario_instancia.save() #salva o comentário

    
    comentarios = Comentarios.objects.filter(aula = aula_id).order_by('-data') # traz todos os comentários da aula ordenado por data
    somente_nomes = [i.usuario.nome for i in comentarios]
    somente_comentarios = [i.comentario for i in comentarios]
    comentarios = list(zip(somente_nomes, somente_comentarios))
 

    return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))


def processa_avaliacao(request): #captura avaliação do usuário
    if request.session.get('usuario'): # verifica se está logado

        avaliacao = request.POST.get('avaliacao') #qual usuário fez a avaliação
        aula_id = request.POST.get('aula_id') 
        
        usuario_id = request.session.get('usuario')

        usuario_avaliou = NotasAulas.objects.filter(aula_id = aula_id).filter(usuario_id = usuario_id) # verifica se há alguma avaliação anterior

        if not usuario_avaliou:  #captura avaliação de usuário que não avaliou ainda
            nota_aulas = NotasAulas(aula_id = aula_id,
                                    nota = avaliacao,
                                    usuario_id = usuario_id,
                                    )
            nota_aulas.save()
            return redirect(f'/home/aula/{aula_id}')
        else:
            return redirect('/auth/login/')

    else:
        return redirect('/auth/login/')

      