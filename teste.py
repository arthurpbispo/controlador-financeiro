# from cryptography.fernet import Fernet

# chave = Fernet.generate_key()
# fernet = Fernet(chave)

# mensagem = "Essa e uma mensagem confidencial"

# mensagem_byte = mensagem.encode()

# criptografado = fernet.encrypt(mensagem_byte)
# print('Criptografado: ', criptografado )

# mensagem_descripto = fernet.decrypt(criptografado)
# print(f'\n {mensagem_descripto.decode()}')

# from datetime import datetime

# def data_atual():
#     hoje = datetime.now()
#     data = hoje.strftime('%d/%m/%y')

#     print(data)


# data_atual()

# lista = [
#     (1, 42, "entrada", 150.00, "Freelance", "2026-05-29"),
#     (2, 42, "saida", 50.0, "Supermercado", "2026-05-29")
# ]

# for transacao in lista:
#     valor = transacao[3]
#     print(valor)

# from uteis.banco import iniciar_banco

# conexao = iniciar_banco()

# cursor = conexao.cursor()

# cursor.execute("SELECT tipo, valor FROM transacoes WHERE usuario_id = ?", (1,))

# transacoes = cursor.fetchall()

# data = {
#         'tipo': [],
#         'valor': []
# }

# soma_dos_valores = 0

# for i, (tipo, valor) in enumerate(transacoes):
#     data['tipo'].append(tipo)
#     data['valor'].append(valor)

#     tipo_minusculo = tipo.lower()
        
#     soma_dos_valores += valor

# print(soma_dos_valores)


    








