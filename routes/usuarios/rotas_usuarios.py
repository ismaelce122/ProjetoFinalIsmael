from flask import render_template, session, redirect, url_for, request, Blueprint, flash
from config import banco as db
from auth import login_required
import pymysql
import pytz
import bcrypt

usuarios_bp = Blueprint("usuarios", __name__, template_folder='usuarios_templates', static_folder='usuarios_static')

@usuarios_bp.route("/clientes/cadastrar", methods = ['GET', 'POST'])
@login_required
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

@usuarios_bp.route("/usuario", methods = ['GET', 'POST'])
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

@usuarios_bp.route('/clientes')
@login_required
def BuscarClientes():
    tz = pytz.timezone('America/Fortaleza')
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM clientes ORDER BY nome ASC'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for cliente in resultado:
            horaFortaleza = cliente['criado_em'].astimezone(tz)
            cliente['criado_em'] = horaFortaleza
            data = cliente['criado_em'].strftime("%d/%m/%Y")
            hora = cliente['criado_em'].strftime("%H:%M:%S")
            cliente['criado_em'] = data
            cliente['hora'] = hora
        return render_template('clientes.html', listaClientes = resultado)
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

@usuarios_bp.route("/login", methods = ['GET', 'POST'])
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
                    return redirect(url_for('Loader'))
                else:
                    print('Senha Incorreta!!!')
                    flash("senha incorreta!!!", "danger")
                    return redirect(url_for('usuarios.Login'))
                    
            else:
                print('E-mail Incorreto!!!')
                flash("e-mail incorreto!!!", "danger")
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

@usuarios_bp.route("/clientes/editar/<int:id>", methods = ['GET', 'POST'])
@login_required
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

@usuarios_bp.route("/clientes/deletar/<int:id>")
@login_required
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