import os
import json
from cryptography.fernet import Fernet

def cripto_senha(usuario ,senha):
    chave = Fernet.generate_key()
    fernet = Fernet(chave)

    senha_byte = senha.encode("utf-8")

    senha_cripto = fernet.encrypt(senha_byte)
    
    return senha_cripto, chave

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
