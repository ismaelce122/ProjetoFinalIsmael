from config import banco
import pymysql

def CadastrarClientes(nome, telefone, email, documento, endereco, senha):
    sql = 'INSERT INTO clientes (nome, telefone, email, documento, endereco, senha) VALUES (%s, %s, %s, %s, %s, %s)'
    try:
        conexao = banco.ConectarBanco()
        cursor = conexao.cursor()
        cursor.execute(sql, (nome, telefone, email, documento, endereco, senha))
        conexao.commit()
        return f'<h2>Cadastro Efetuado com Sucesso!!!</h2>'
    except pymysql.MySQLError as e:
        print('-----------------------------------------------')
        print(f'Erro no banco de dados: {e.args[0]}')
        print(f'Mensagem do Erro: {e.args[1]}')
        print('-----------------------------------------------')
        return f'<h2>Erro no banco de dados: {e}</h2>'
    except Exception as e:
        erro = True
        print(f'Houve um erro: {e}')
        return f'<h2>Houve um erro: {e}</h2>'
    finally:
        conexao.close()
        cursor.close()