from uteis.banco import iniciar_banco
from uteis.banco import buscar_id
from uteis.banco import pegar_senha_cripto
from uteis.banco import cadastrar_usuario
from uteis.banco import adicionar_saldo, retirar_saldo
from uteis.banco import extrato_dict_to_SQL_nubank
from uteis.banco import adicionar_limite, aviso_limite
from uteis.banco import to_historico_transacoes, pegar_historico_transacoes
from uteis.uteis import cripto_senha
from uteis.uteis import descripto_senha
from uteis.uteis import pegar_chave_usuario
from uteis.uteis import analise_extrato
from uteis.uteis import salvar_cadastro_json
from uteis.uteis import data_atual
from uteis.uteis import to_excel, to_pdf, extrato_to_dict


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
    def __init__(self, id, usuario, tipo, valor, descricao, data):
        self.id = id
        self.usuario = usuario
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.data = data
        

class Saida:
    def __init__(self, id, usuario, tipo, valor, descricao, data):
        self.id = id
        self.usuario = usuario
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.data = data
        
        
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
               usuario_limite, soma_dos_gastos = aviso_limite(conexao, id_logado, nome_usuario)

               if usuario_limite:
                   print(f'\nVoce estrapolou o limite salvo, voce gastou {soma_dos_gastos}')

               while True: 
                ask2 = input(f'\n{nome_usuario}, o que voce deseja fazer \n(1)Adicionar saldo:  \n(2)Retirar dinherio: \n(3)Ver suas transacoes: \n(4)Adicionar extrato de banco: \n(5)Adicionar ou alterar limite da conta \n(6)Sair, deslogar')
                if ask2 == '1':
                    valor = float(input('\nQuanto voce deseja adicionar a sua conta: '))
                    descricao = input('\nDe uma descricao a sua transacao: ')
                    data = data_atual()
                    tipo = 'entrada'

                    entrada = Entrada(id_logado, nome_usuario, tipo, valor, descricao, data)    

                    adicionar_saldo(conexao, id_logado, entrada.valor)
                    to_historico_transacoes(conexao, id_logado, entrada.tipo, entrada.valor, entrada.descricao, entrada.data)



                elif ask2 == '2':
                    valor = float(input('\nQuanto voce deseja retirar da sua conta: '))
                    descricao = input('\nDe um descricao a sua transacao: ')
                    data = data_atual()
                    tipo = 'saida'
                    
                    retirar = Saida(id_logado, nome_usuario, tipo, valor, descricao, data)

                    retirar_saldo(conexao, id_logado, retirar.valor)
                    to_historico_transacoes(conexao, id_logado, tipo, retirar.valor, retirar.descricao, retirar.data)

                elif ask2 == '3':
                    todas_as_transacoes = pegar_historico_transacoes(conexao, id_logado)

                    ask4 = int(input('\n(1)Voce gostaria de ver todas as suas transações: \n(2)Insira as datas que gostaria de filtrar as transacoes '))
                    
                    if ask4 == 1:
                        for transacao in todas_as_transacoes:
                            tipo = transacao[2]
                            valor = transacao[3]
                            descricao = transacao[4]
                            data = transacao[5]

                        print(f'\nTransacao no valor de {valor} com a descricao de {descricao} no dia {data}')

                        ask3 = int(input('\nVoce deseja levar esses dados a uma planilha ? \n(1)Sim(Excel) \n(2)Sim(PDF) \n(3)Não'))   

                        if ask3 == 1:
                          to_excel(todas_as_transacoes)
                          print('\nPlanilha (financas.xlsx) criada com sucesso')
                    
                        elif ask3 == 2:
                          to_pdf(todas_as_transacoes)

                    elif ask4 == 2:
                        data_incial = input('Insira a data inical: ')
                        data_final = input('Isira a data final: ')



                    

                elif ask2 == '4':
                    caminho_arquivo = input('Passe o caminho do arquivo do seu extrato: ')
                    
                    extrato_dict = extrato_to_dict(caminho_arquivo)

                    analise_extrato(extrato_dict)

                    extrato_dict_to_SQL_nubank(conexao, id_logado, extrato_dict)
                        
                elif ask2 == '5':
                    novo_limite = float(input('\nQual limite voce deseja adicionar a sua conta: '))
                    adicionar_limite(conexao, novo_limite, id_logado)

                elif ask2 == '6':
                    break

            else:
                print("\n[-] Erro: Usuário ou senha incorretos.")

            

            
        








    conexao.close()


    