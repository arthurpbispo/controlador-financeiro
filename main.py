from uteis.banco import iniciar_banco
from uteis.banco import buscar_id
from uteis.banco import pegar_senha_cripto
from uteis.banco import cadastrar_usuario
from uteis.banco import adicionar_saldo, retirar_saldo
from uteis.banco import to_historico_transacoes
from uteis.uteis import cripto_senha
from uteis.uteis import descripto_senha
from uteis.uteis import pegar_chave_usuario
from uteis.uteis import salvar_cadastro_json
from uteis.uteis import data_atual


class Usuario:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha

    def para_dict(self):
        return {
            "usuario": self.usuario,
            "chave_senha": self.senha
        }

class Entrada:
    def __init__(self, id, usuario, valor, descricao, data):
        self.id = id
        self.usuario = usuario
        self.valor = valor
        self.descricao = descricao
        self.data = data
        

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

        id_logado = buscar_id(conexao, nome_usuario)

        if id_logado is not None:
            chave_descripto = pegar_chave_usuario(nome_usuario)
            senha_cripto = pegar_senha_cripto(conexao, id_logado)
            senha_descripto = descripto_senha(senha_cripto, chave_descripto)

            if senha == senha_descripto:
               while True: 
                ask2 = input(f'\n{nome_usuario}, o que voce deseja fazer \n(1)Adicionar saldo:  \n(2)Retirar dinherio: \n(3)Sair, deslogar')
                if ask2 == '1':
                    valor = float(input('\nQuanto voce deseja adicionar a sua conta: '))
                    descricao = input('\nDe uma descricao a sua transacao: ')
                    data = data_atual
                    entrada = Entrada(id_logado, nome_usuario, valor, descricao, data)

                    adicionar_saldo(conexao, id_logado, entrada.valor)
                    to_historico_transacoes(conexao, id_logado, entrada.valor, entrada.descricao, entrada.data())



                elif ask2 == '2':
                    valor = float(input('\nQuanto voce deseja retirar da sua conta: '))
                    retirar = Saida(valor)

                    retirar_saldo(conexao, id_logado, retirar.valor)

                elif ask2 == '3':
                    break

            else:
                print("\n[-] Erro: Usuário ou senha incorretos.")

            

            
        








    conexao.close()


    