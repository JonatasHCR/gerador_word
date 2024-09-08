from django.shortcuts import render

from pathlib import Path
from os import walk
#salvando o caminho do modelo
caminho_modelo = Path(__file__).parent / 'functions' / 'modelos'

# Create your views here.
def home(request):
    context_ = {'modelos': walk(caminho_modelo)}
    return render(
        request,
        'home/index.html',
        context_
    )

def dados(request):
    context_ = {'modelos': walk(caminho_modelo)}
    if request.method == 'POST':
        match request.POST.get('botao'):
            case 'formulario_dados':
                from .functions.formatando_dados import FormatAll
                from .functions.alterando_documento import gerando_documento
                
                dados = FormatAll(request.POST.items())
                gerando_documento(dados.dados_dict.items(),caminho_modelo)
            case _: 
                context_.update([('nome_modelo',request.POST.get('botao'))])   
    return render(
        request,
        'home/dados.html',
        context_
    )

def criar_model(request):
    context_ = {'modelos': walk(caminho_modelo)}
    return render(
        request,
        'home/criar_modelo.html',
        context_
    )