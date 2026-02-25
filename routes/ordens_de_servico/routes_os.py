from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from config import banco as db
import pymysql

ordens_bp = Blueprint("ordens", __name__, url_prefix='/ordens_de_servico', template_folder='os_templates', static_folder='os_static')

@ordens_bp.route("/", methods = ['GET', 'POST'])
def OrdensServico():
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM os JOIN clientes ON os.id_cliente = clientes.id JOIN mecanicos ON os.id_mecanico = mecanicos.id'
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return render_template("os.html", resultado = resultado)
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
        pass

@ordens_bp.route("/api/pecas")
def Pecas():
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM pecas ORDER BY nome ASC'
        cursor.execute(sql)
        pecas = cursor.fetchall()
        return jsonify(pecas)
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

@ordens_bp.route("/criar_ordem", methods = ['GET', 'POST'])
def CadastrarOs():
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM clientes ORDER BY nome ASC'
            cursor.execute(sql)
            clientes = cursor.fetchall()
            sql = 'SELECT * FROM mecanicos ORDER BY nome ASC'
            cursor.execute(sql)
            mecanicos = cursor.fetchall()
            return render_template("cadastrar_os.html", mecanicos = mecanicos, clientes = clientes)
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
        os = {
                'id_cliente': request.form.get('id_cliente'),
                'id_mecanico': request.form.get('id_mecanico'),
                'status_os': request.form.get('status_os'),
                'problema_relatado': request.form.get('problema_relatado'),
                'diagnostico': request.form.get('diagnostico')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO os (id_cliente, id_mecanico, status_os, problema, diagnostico) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (os['id_cliente'], os['id_mecanico'], os['status_os'], os['problema_relatado'], os['diagnostico']))
            conexao.commit()
            return redirect(url_for('ordens.OrdensServico'))
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

@ordens_bp.route("/itens_os/<int:id_os>/<cliente>", methods = ['GET', 'POST'])
def ItensOs(id_os, cliente):
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM pecas ORDER BY nome ASC'
            cursor.execute(sql)
            pecas = cursor.fetchall()
            sql = 'SELECT * FROM os WHERE id = %s ORDER BY id ASC'
            cursor.execute(sql, id_os)
            idOs = cursor.fetchone()
            sql = 'SELECT * FROM clientes WHERE nome = %s ORDER BY id ASC'
            cursor.execute(sql, cliente)
            nomeCliente = cursor.fetchone()
            return render_template("cadastrar_itens_da_os.html", pecas = pecas, idOs = idOs, nomeCliente = nomeCliente)
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
        id_os = request.form.get('id_os')
        pecas = request.form.getlist('peca[]')
        quantidades = request.form.getlist('quantidade[]')
        print(pecas)
        print(quantidades)
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            for peca, quantidade in zip(pecas, quantidades):
                nome, preco = peca.split('-')
                sql = 'INSERT INTO itens_os (id_os, nome, quantidade, preco) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql, (id_os, nome, quantidade, preco))
            conexao.commit()
            return redirect(url_for('ordens.OrdensServico'))
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