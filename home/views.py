from django.shortcuts import render

from pathlib import Path
from os import walk

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
    if request.method == 'POST':
        from .functions.trabalho import format_date,escrever_money,format_dinheiro,documet_alterar
        dados_dict = {}
        for chave,valor in request.POST.items():
            valor = valor.strip()
            match chave:
                case 'csrfmiddlewaretoken':
                    continue
                case 'hhh':
                    dinheiro_escrito = escrever_money(valor)
                    valor = format_dinheiro(valor)
                    lista = [['LLL',dinheiro_escrito],[chave.upper(),valor]]
                    dados_dict.update(lista)
                    continue
                case 'aaa':
                    valor = format_date(valor)
                    dados_dict.update([(chave.upper(),valor)])
                    continue
                case 'xxx':
                    valor = f'Medição n.º {valor}'
                    dados_dict.update([(chave.upper(),valor)])

     
            dados_dict.update([(chave.upper(),valor)])
        documet_alterar(dados_dict.items(),caminho_modelo)
        print(dados_dict.items())
             
    return render(
        request,
        'home/dados.html'
    )