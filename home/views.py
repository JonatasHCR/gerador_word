from django.shortcuts import render

from pathlib import Path
from os import walk
from sqlite3 import IntegrityError
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
                valores_ante = []
                for chave,valor in request.POST.items():
                    match chave:
                        case 'csrfmiddlewaretoken':
                            continue
                        case 'nome_modelo':
                            context_.update([(chave,valor)])
                            from .functions.criar_db_modelo import retirar
                            dados = retirar(valor)
                            combinadas = [(dados[1][i], dados[0][i], dados[2][i]) for i in range(len(dados[0]))]
                            context_.update([('dados_comp',combinadas)])
                            continue
                        case 'caminho_saida':
                            continue
                        case 'arquivo_saida':
                            continue
                        case 'botao':
                            continue
                    valores_ante.append(valor)
                from .functions.formatando_dados import FormatAll
                from .functions.alterando_documento import gerando_documento
                
                dados = FormatAll(request.POST.items())
                gerando_documento(dados.dados_dict.items(),caminho_modelo)
            case _:
                nome_modelo = request.POST.get('botao')
                context_.update([('nome_modelo',nome_modelo)])
                
                from .functions.criar_db_modelo import retirar
                dados = retirar(nome_modelo)
                combinadas = [(dados[1][i], dados[0][i], dados[2][i]) for i in range(len(dados[0]))]
                context_.update([('dados_comp',combinadas)])

    return render(
        request,
        'home/dados.html',
        context_
    )

def criar_model(request):
    context_ = {'modelos': walk(caminho_modelo)}
    if request.method == 'POST':
        match request.POST.get('botao'):
            case 'variaveis_modelo':
                import string
                quant_var = int(request.POST.get('quant_var'))
                a = list(string.ascii_uppercase)
                nome_modelo = request.POST.get('nome_modelo')
                context_.update([('quant_var',((n+1, a[n]*3) for n in range(quant_var))),('nome_modelo', nome_modelo),('formulario_modelo','ok')])
            
            case 'criando_modelo':
                from .functions.alterando_documento import gerando_modelo
                gerando_modelo(request.POST.get('nome_modelo'))

                from .functions.criar_db_modelo import inserir
                nome = request.POST.get('nome_modelo')+'.doc'
                variaveis = request.POST.getlist('variavel')
                ref_variaveis = request.POST.getlist('ref_variavel')
                default_variavel = request.POST.getlist('default_variavel')
                try:
                    inserir(nome,variaveis,ref_variaveis,default_variavel)
                except IntegrityError:
                    context_.update([('error_mensagem', 'JA EXISTE UM MODELO COM ESSE NOME')])
    return render(
        request,
        'home/criar_modelo.html',
        context_
    )

def modificar(request):
    context_ = {'modelos': walk(caminho_modelo)}
    if request.method == 'POST':
        print(request.POST)
    return render(
        request,
        'home/modificar_modelo.html',
        context_
    )