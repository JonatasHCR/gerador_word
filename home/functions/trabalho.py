import docx
from num2words import num2words

def format_date(date:str):
    if date.count('/') < 2 :
        return date
    meses = {'janeiro':'01', 'fevereiro':'02', 'março':'03', 'abril':'04', 
           'maio':'05', 'junho': '06', 'julho':'07', 'agosto': '08', 
           'setembro':'09', 'outubro':'10', 'novembro':'11', 'dezembro':'12'}
    
    date = date.replace('/', ' de ')
    for mes,numero in meses.items():
        dia_,mes_,ano_ = date.split(' de ')
        if numero in mes_:
            date = ' de '.join([dia_,mes,ano_])
            return date

def escrever_money(dinheiro: str):
    dinheiro = dinheiro.strip()
    dinheiro = dinheiro.replace('.','')
    if 'R$' in dinheiro:
        dinheiro = dinheiro.replace('R$','')
    
    if ',' in dinheiro:
    
        reais,centavos = dinheiro.split(',')
        if 0 != int(centavos):
            reais = num2words(int(reais),lang='pt-br') +' reais e '
            centavos = num2words(int(centavos),lang='pt-br')+ ' centavos'
            dinheiro_escrito: str = reais + centavos
            dinheiro_escrito = dinheiro_escrito.replace('mil','mil,')
            dinheiro_escrito = dinheiro_escrito.replace('milhões', 'milhões,')
            dinheiro_escrito = dinheiro_escrito.replace('milhão','milhão,')
            return dinheiro_escrito
        else:
            dinheiro_escrito = num2words(int(reais),lang='pt-br') + ' reais'
            dinheiro_escrito = dinheiro_escrito.replace('mil','mil,')
            dinheiro_escrito = dinheiro_escrito.replace('milhões', 'milhões,')
            dinheiro_escrito = dinheiro_escrito.replace('milhão','milhão,')
            return dinheiro_escrito

    dinheiro_escrito = num2words(int(dinheiro),lang='pt-br') + ' reais'
    dinheiro_escrito = dinheiro_escrito.replace('mil','mil,')
    dinheiro_escrito = dinheiro_escrito.replace('milhões', 'milhões,')
    dinheiro_escrito = dinheiro_escrito.replace('milhão','milhão,')
    return dinheiro_escrito

def format_dinheiro(dinheiro:str):
    dinheiro = dinheiro.strip()
    if 'R$' in dinheiro and ',' in dinheiro:
        return dinheiro
    if ',' not in dinheiro:
        dinheiro = dinheiro.replace('R$', '')
        dinheiro = f'R${dinheiro},00'
        return dinheiro
    
    return f'R$ {dinheiro}'

        
def replace_text_in_docx(paragraph, subst_text_list: list):
    for old_text in subst_text_list:
        new_text = old_text[1]
        if old_text[0] in paragraph.text:
            linha = paragraph.runs
            for item in linha:
                if old_text[0] in item.text:
                    item.text = item.text.replace(old_text[0], new_text)

def documet_alterar(variables_values: list, caminho_modelo):
    for tuplas in variables_values:
        match tuplas[0]:
            case 'NOME_MODELO':
                path_file_model = tuplas[1].strip() + '.doc'
            case 'CAMINHO_SAIDA':
                caminho_saida = tuplas[1]
            case 'ARQUIVO_SAIDA':
                path_file_save = tuplas[1].strip() + '.doc'
        continue
    caminho_modelo = caminho_modelo / path_file_model
    caminho_saida = f'{caminho_saida}\\{path_file_save}'
    try:
        doc = docx.Document(caminho_modelo)
        for linha in doc.paragraphs:
                replace_text_in_docx(linha,variables_values)
        doc.save(caminho_saida)
    except:
        print('Não foi possivel salvar o arquivo')
