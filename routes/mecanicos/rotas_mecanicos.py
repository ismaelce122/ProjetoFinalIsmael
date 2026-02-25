from flask import render_template, redirect, request, url_for, Blueprint
from auth import login_required
from config import banco as db
import pymysql

mecanicos_bp = Blueprint("mecanicos", __name__, url_prefix='/mecanicos', template_folder='mecanicos_templates', static_folder='mecanicos_static')

@mecanicos_bp.route("/")
@login_required
def BuscarMecanicos():
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM mecanicos ORDER BY nome ASC'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template('mecanicos.html', resultado = resultado)
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

@mecanicos_bp.route("/cadastrar", methods = ['GET', 'POST'])
@login_required
def CadastrarMecanicos():
    if request.method == 'GET':
        return render_template("cadastrarmecanicos.html")
    elif request.method == 'POST':
        mecanico = {
                'nome': request.form.get('nome'),
                'especialidade': request.form.get('especialidade')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO mecanicos (nome, especialidade) VALUES (%s, %s)'
            cursor.execute(sql, (mecanico['nome'], mecanico['especialidade']))
            conexao.commit()
            return redirect(url_for('mecanicos.BuscarMecanicos'))
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

@mecanicos_bp.route("/editar/<int:id>", methods = ['GET', 'POST'])
@login_required
def EditarMecanico(id):
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM mecanicos WHERE id = %s'
            cursor.execute(sql, (id, ))
            resultado = cursor.fetchone()
            return render_template('editar_mecanicos.html', resultado = resultado)
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
        mecanico = {
                'nome': request.form.get('nome'),
                'especialidade': request.form.get('especialidade')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'UPDATE mecanicos SET nome = %s, especialidade = %s WHERE id = %s'
            cursor.execute(sql, (mecanico['nome'], mecanico['especialidade'], id))
            conexao.commit()
            return redirect(url_for('mecanicos.BuscarMecanicos'))
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

@mecanicos_bp.route("/deletar/<int:id>")
@login_required
def DeletarMecanico(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM mecanicos WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('mecanicos.BuscarMecanicos'))
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