import os
import json
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
