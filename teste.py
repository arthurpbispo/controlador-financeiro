# from cryptography.fernet import Fernet

# chave = Fernet.generate_key()
# fernet = Fernet(chave)

# mensagem = "Essa e uma mensagem confidencial"

# mensagem_byte = mensagem.encode()

# criptografado = fernet.encrypt(mensagem_byte)
# print('Criptografado: ', criptografado )

# mensagem_descripto = fernet.decrypt(criptografado)
# print(f'\n {mensagem_descripto.decode()}')

from datetime import datetime

def data_atual():
    hoje = datetime.now()
    data = hoje.strftime('%d/%m/%y')

    print(data)


data_atual()


