import sqlite3
from uteis.uteis import tratar_data

def iniciar_banco():
    conexao = sqlite3.connect("financas.db")
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        saldo REAL DEFAULT 0.0,
        limite REAL DEFAULT 0.0
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tipo TEXT,
        valor REAL,
        descricao TEXT,
        data DATE,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )""")
    conexao.commit()
    return conexao

def cadastrar_usuario(conexao, usuario, senha):
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conexao.commit()
        print('\nUsuario cadastrado com sucesso')
    except sqlite3.IntegrityError:
        print('\nErro: Este nome ja existe')

def adicionar_saldo(conexao, id_usuario, valor):
    cursor = conexao.cursor()

    cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (valor, id_usuario))

    conexao.commit()
    print(f'\n O valor de {valor:.2f} foi adicionado com sucesso a sua conta')

def retirar_saldo(conexao, id_usuario, valor):
    cursor = conexao.cursor()

    cursor.execute("UPDATE usuarios SET saldo = saldo - ?   WHERE id = ?", (valor, id_usuario))

    conexao.commit()
    print(f'\n O valor de {valor} foi retirado da sua conta')

def buscar_id(conexao, nome_usuario):
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (nome_usuario,))
    resultado = cursor.fetchone()   

    if resultado:
        usuario_id = resultado[0]
        return usuario_id
    else:
        print('Usuario nao encontrado')
        return None
    
def pegar_senha_cripto(conexao, id_logado):
    cursor = conexao.cursor()

    cursor.execute("SELECT senha FROM usuarios WHERE id = ? ", (id_logado,))
    resultado = cursor.fetchone()

    if resultado:
        chave_cripto = resultado[0]
        return chave_cripto
    else:
        return None
    
def to_historico_transacoes(conexao, id_logado, tipo, valor, descricao, data,):
    cursor = conexao.cursor()

    cursor.execute("""
      INSERT INTO transacoes (
      usuario_id, tipo, valor, descricao, data)
      VALUES (?, ?, ?, ?, ?)
    """, (id_logado, tipo, valor, descricao, data)) 
    
    conexao.commit()

def pegar_historico_transacoes(conexao, id_logado):
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM transacoes WHERE usuario_id = ?", (id_logado,))
    resultado = cursor.fetchall()

    return resultado

def extrato_dict_to_SQL_nubank(conexao , id_logado, extrato_dict):
    cursor = conexao.cursor()

    """
    1. Logica para pegar todas as transacoes salvas no banco (lista de tuplas)

    2. Tratar se nescessario

    3. Dentro do for verificar cada linha do extrato dict verificar se existe alguma transacao igual

    4. Se existir(Nao entra no banco) Se nao existir(Entra no banco)
    """

    cursor.execute("SELECT * FROM transacoes WHERE usuario_id = ?", (id_logado,))

    transacoes_SQL_usuario = cursor.fetchall()

    for linha_extrato in extrato_dict:
        valor_absoluto = abs(float(linha_extrato['Valor']))

        data = linha_extrato['Data']
        data_to_banco = tratar_data(data)

        Descricao_e_tipo = linha_extrato['Descrição']

        if ' - ' in Descricao_e_tipo:
            tipo, descricao = Descricao_e_tipo.split(' - ', 1)
        else:
            tipo = Descricao_e_tipo
            descricao = Descricao_e_tipo  

        achou_igual = True

        for transacao in transacoes_SQL_usuario:

            if (str(transacao[5]).strip() == str(data_to_banco).strip() and
                float(transacao[3]) == valor_absoluto and
                str(transacao[2]).strip() == str(tipo).strip()
            ):

                achou_igual = False

        if achou_igual:
            cursor.execute("""
                INSERT INTO transacoes (
                    usuario_id, tipo, valor, descricao, data
                ) VALUES (?, ?, ?, ?, ?)
            """, (id_logado, tipo, valor_absoluto, descricao, data_to_banco))
        else:
            print(f"Transação ignorada (já cadastrada no banco): {descricao}")


    conexao.commit()

def adicionar_limite(conexao, novo_limite, id_logado):
    cursor = conexao.cursor()

    if novo_limite is None:
        print('O limite nao possui valor')
    
    else:
        cursor.execute("UPDATE usuarios SET limite = ? WHERE id = ?", (novo_limite, id_logado))
        print('\nLimite adicionado com sucesso')

        conexao.commit()

def aviso_limite(conexao, id_logado, nome_usuario):
    cursor = conexao.cursor()

    cursor.execute("SELECT tipo, valor FROM transacoes WHERE usuario_id = ?", (id_logado,))

    transacoes = cursor.fetchall()

    data = {
        'tipo': [],
        'valor': []
    }

    soma_dos_valores = 0

    for i, (tipo, valor) in enumerate(transacoes):
        data['tipo'].append(tipo)
        data['valor'].append(valor)  

        tipo_minusculo = tipo.lower()
        
        if 'enviada' in tipo_minusculo or 'compra' in tipo_minusculo or 'saida' in tipo_minusculo:
            soma_dos_valores += valor
    
    cursor.execute("SELECT limite FROM usuarios WHERE usuario = ?", (nome_usuario,))
    limite_usuario = cursor.fetchone()

    soma_dos_valores_int = int(soma_dos_valores)
    limite_usuario_int = int(limite_usuario[0])

    try:
        porcentagem = soma_dos_valores_int/limite_usuario_int * 100

    except ZeroDivisionError:
        print('O usuario nao possui limite')
        porcentagem = 0
    
    if porcentagem >= 100:
        return True, soma_dos_valores_int
    else:
        return False, soma_dos_valores_int
    
        

