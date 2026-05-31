import sqlite3

def iniciar_banco():
    conexao = sqlite3.connect("financas.db")
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        saldo REAL DEFAULT 0.0
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tipo TEXT,
        valor REAL,
        descricao TEXT,
        data TEXT,
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

def extrato_dict_to_SQL(conexao , id_logado, extrato_dict):
    cursor = conexao.cursor()

    for linha_extrato in extrato_dict:
        valor_absoluto = abs(float(linha_extrato['Valor']))

        data = linha_extrato['Data']

        Descricao_e_tipo = linha_extrato['Descrição']

        if ' - ' in Descricao_e_tipo:
            tipo, descricao = Descricao_e_tipo.split(' - ', 1)
        else:
            tipo = Descricao_e_tipo
            descricao = Descricao_e_tipo  

        usuario_id = id_logado

        cursor.execute("""
          INSERT INTO transacoes (
          usuario_id, tipo, valor, descricao, data)
          VALUES (?, ?, ?, ?, ?)
        """, (id_logado, tipo, valor_absoluto, descricao, data))

        conexao.commit()











