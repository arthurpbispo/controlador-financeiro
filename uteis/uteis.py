import os
import json
import pandas as pd
from weasyprint import HTML
from datetime import datetime
from cryptography.fernet import Fernet

def cripto_senha(usuario ,senha):
    chave = Fernet.generate_key()
    fernet = Fernet(chave)

    senha_byte = senha.encode("utf-8")

    senha_cripto = fernet.encrypt(senha_byte)
    
    return senha_cripto, chave

def pegar_chave_usuario(usuario_logado):
    caminho_json = 'chaves_cripto/chaves.json'

    if os.path.exists(caminho_json) and os.path.getsize(caminho_json) > 0:
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            lista_cadastros = json.load(arquivo)

        for cadastro in lista_cadastros:
            if cadastro.get("usuario") == usuario_logado:
                return cadastro.get("chave_senha")
            
    return None

def salvar_cadastro_json(cadastro):
    caminho_json = 'chaves_cripto/chaves.json'

    if os.path.exists(caminho_json) and os.path.getsize(caminho_json) > 0:
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            lista_usuarios = json.load(arquivo)
    else:
        lista_usuarios = []

    lista_usuarios.append(cadastro)

    with open(caminho_json, "w", encoding='utf-8') as arquivo:
        json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)

def descripto_senha(senha_cripto, chave_descripto):
    if isinstance(chave_descripto, str):
        chave_descripto_bytes = chave_descripto.encode("utf-8")
    else:
        chave_descripto_bytes = chave_descripto

    if isinstance(senha_cripto, str):
        senha_cripto_bytes = senha_cripto.encode("utf-8")
    else:
        senha_cripto_bytes = senha_cripto
    
    fernet = Fernet(chave_descripto_bytes)
    senha_descriptografada_bytes = fernet.decrypt(senha_cripto_bytes)

    return senha_descriptografada_bytes.decode("utf-8")

def data_atual():
    hoje = datetime.now()
    data = hoje.strftime('%d/%m/%y')

    return data

def to_excel(todas_as_transacoes):
    pre_df = {
        'tipo': [],
        'valor': [],
        'descricao': [],
        'data': []
    }
    
    for transacao in todas_as_transacoes:
        pre_df['tipo'].append(transacao[2])
        pre_df['valor'].append(transacao[3])
        pre_df['descricao'].append(transacao[4])
        pre_df['data'].append(transacao[5])

    df = pd.DataFrame(pre_df)
    
    df.index += 1
    df.to_excel('Financas.xlsx')

def to_pdf(todas_as_transacoes):
    data = {
        'tipo': [],
        'valor': [],
        'descricao': [],
        'data': []
    }

    for transacao in todas_as_transacoes:
        data['tipo'].append(transacao[2])
        data['valor'].append(transacao[3])
        data['descricao'].append(transacao[4])
        data['data'].append(transacao[5])

    df = pd.DataFrame(data)
    
    df_html = df.to_html(index=False, classes='table table-striped')
    
    HTML(string=df_html).write_pdf('Financas.pdf')


def extrato_to_dict(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, encoding='utf-8')
    df_dict = df.to_dict(orient='records')

    return df_dict

def analise_extrato(extrato_dict):
    soma_dos_valores_entrada = 0
    soma_dos_valores_saida = 0    

    for i in extrato_dict:
        descricao_minuscula = i['Descrição'].lower()

        if 'compra' in descricao_minuscula or 'enviada' in descricao_minuscula:
            soma_dos_valores_saida += i['Valor']

        else:
            soma_dos_valores_entrada += i['Valor']

    print(f'\nNesse extrato voce fez essas transacoes Entrada: {soma_dos_valores_entrada:.2f} Saida: {soma_dos_valores_saida:.2f}')

def tratar_data(data):
    data_read = datetime.strptime(data, "%d/%m/%Y")

    data_to_banco = data_read.strftime("%Y-%m-%d")

    return data_to_banco


    
    
    
            

