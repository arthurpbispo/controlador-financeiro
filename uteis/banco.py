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

def login_usuario(conexao, usuario, senha):
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, usuario, saldo FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    return None

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







