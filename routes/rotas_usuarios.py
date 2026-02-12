from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from config import banco as db
import pymysql
import pytz
import bcrypt

usuarios = Blueprint("usuarios", __name__)

@usuarios.route("/clientes/cadastrar", methods = ['GET', 'POST'])
def CadastrarClientes():
    if request.method == 'GET':
        return render_template("cadastrarclientes.html")
    elif request.method == 'POST':
        senha = request.form.get('senha')
        cliente = {
                'nome': request.form.get('nome'),
                'telefone': request.form.get('telefone'), 
                'email': request.form.get('email'),
                'documento': request.form.get('documento'),
                'endereco': request.form.get('endereco'),   
                'senhaHash': bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO clientes (nome, telefone, email, documento, endereco, senha) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (cliente['nome'], cliente['telefone'], cliente['email'], cliente['documento'], cliente['endereco'], cliente['senhaHash']))
            conexao.commit()
            return redirect(url_for('usuarios.BuscarClientes'))
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

@usuarios.route("/usuario", methods = ['GET', 'POST'])
def CadastrarUsuario():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        senha = request.form.get('senha')
        cliente = {
                'nome': request.form.get('nome'),
                'telefone': request.form.get('telefone'), 
                'email': request.form.get('email'),
                'documento': request.form.get('documento'),
                'endereco': request.form.get('endereco'),   
                'senhaHash': bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO clientes (nome, telefone, email, documento, endereco, senha) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (cliente['nome'], cliente['telefone'], cliente['email'], cliente['documento'], cliente['endereco'], cliente['senhaHash']))
            conexao.commit()
            return redirect(url_for('usuarios.Login'))
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

@usuarios.route('/clientes')
def BuscarClientes():
    tz = pytz.timezone('America/Fortaleza')
    listaClientes = []
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM clientes ORDER BY nome ASC'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for cliente in resultado:
            horaFortaleza = cliente['criado_em'].astimezone(tz)
            cliente['criado_em'] = horaFortaleza
            listaClientes.append(cliente)
        for lista in listaClientes:
            print(lista['criado_em'])
        return render_template('clientes.html', listaClientes = listaClientes)
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

@usuarios.route("/login", methods = ['GET', 'POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM clientes WHERE email= %s'
            cursor.execute(sql, (email, ))
            resultado = cursor.fetchone()
            if resultado:
                senhaHash = resultado['senha']
                print(f'Usuário Logado: {resultado['nome']}')
                if bcrypt.checkpw(senha.encode('utf-8'), senhaHash.encode('utf-8')):
                    session['usuario_nome'] = resultado['nome']
                    session['usuario_id'] = resultado['id']
                    return redirect(url_for('PainelServicos'))
                else:
                    print('Senha Incorreta!!!')
                    return '''
                            <meta http-equiv="refresh" content="3; url='/login'">
                            <h2 style="text-align: center; margin-top: 20px;">Senha Incorreta!!!</h2>
                            <a href="/login" style="text-align: center; display: block; text-decoration: none; color: white; background-color: #007bff; width: 150px; padding: 10px; border-radius: 5px; margin: auto;"><<< Voltar ao Login</a>
                           ''' 
            else:
                print('E-mail Incorreto!!!')
                return '''
                        <meta http-equiv="refresh" content="3; url='/login'">
                        <h2 style="text-align: center; margin-top: 20px;">E-mail Incorreto!!!</h2>
                        <a href="/login" style="text-align: center; display: block; text-decoration: none; color: white; background-color: #007bff; width: 150px; padding: 10px; border-radius: 5px; margin: auto;"><<< Voltar ao Login</a>
                       '''
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

@usuarios.route("/clientes/editar/<int:id>", methods = ['GET', 'POST'])
def EditarCliente(id):
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM clientes WHERE id = %s'
            cursor.execute(sql, (id, ))
            resultado = cursor.fetchone()
            return render_template('editar_clientes.html', resultado = resultado)
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
    elif request.method == 'POST':
        cliente = {
                'nome': request.form.get('nome'),
                'telefone': request.form.get('telefone'), 
                'email': request.form.get('email'),
                'documento': request.form.get('documento'),
                'endereco': request.form.get('endereco')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'UPDATE clientes SET nome = %s, telefone = %s, email = %s, documento=%s, endereco=%s WHERE id = %s'
            cursor.execute(sql, (cliente['nome'], cliente['telefone'], cliente['email'], cliente['documento'], cliente['endereco'], id))
            conexao.commit()
            return redirect(url_for('usuarios.BuscarClientes'))
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

@usuarios.route("/clientes/deletar/<int:id>")
def DeletarCliente(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM clientes WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('usuarios.BuscarClientes'))
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