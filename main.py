from uteis.banco import iniciar_banco
from uteis.banco import cadastrar_usuario, login_usuario
from uteis.banco import adicionar_saldo, retirar_saldo
from uteis.uteis import cripto_senha
from uteis.uteis import salvar_cadastro_json

class Usuario:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha

    def para_dict(self):
        return {
            "usuario": self.usuario,
            "senha": self.senha
        }

class Entrada:
    def __init__(self, valor):
        self.valor = valor

class Saida:
    def __init__(self, valor):
        self.valor = valor
        
        
if __name__ == "__main__":
    conexao = iniciar_banco()
    print("Banco de dados conectado com sucesso!")
    
    ask1 = int(input('O que voce deseja fazer \n(1)Criar conta \n(2)Logar na conta'))

    if ask1 == 1:
        nome_usuario = input('Qual sera o seu nome de usuario: ').strip()
        senha = input('Qual sera a sua senha: ').strip()
        senha_cripto, chave = cripto_senha(nome_usuario, senha) 

        novo_usuario = Usuario(nome_usuario, senha_cripto)

        cadastrar_usuario(conexao, novo_usuario.usuario, novo_usuario.senha)

        novo_usuario_json = Usuario(nome_usuario, chave.decode())
        salvar_cadastro_json(novo_usuario_json.para_dict())


    elif ask1 == 2:
        nome_usuario = input('Qual e o seu nome de usuario: ').strip()
        senha = input('Digite sua senha: ').strip()

        id_logado = login_usuario(conexao, nome_usuario, senha)
        
        if id_logado is not None:
            print("\n[+] Login realizado com sucesso!")
            
            ask2 = input(f'Olá {nome_usuario}, o que voce deseja fazer \n(1)Adicionar saldo \n(2)Retirar dinherio ')
            if ask2 == '1':
                valor = float(input('Quanto voce deseja adicionar a sua conta: '))
                entrada = Entrada(valor)

                adicionar_saldo(conexao, id_logado, entrada.valor)

            elif ask2 == '2':
                valor = float(input('Quanto voce deseja retirar da sua conta: '))
                retirar = Saida(valor)

                retirar_saldo(conexao, id_logado, retirar.valor)

        else:
            print("\n[-] Erro: Usuário ou senha incorretos.")








    conexao.close()


    