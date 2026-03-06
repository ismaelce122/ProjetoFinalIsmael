from flask import render_template, redirect, url_for, request, jsonify, Blueprint, flash
from auth import login_required
from config import banco as db
import pymysql
import pytz

ordens_bp = Blueprint("ordens", __name__, url_prefix='/ordens_de_servico', template_folder='os_templates', static_folder='os_static')

@ordens_bp.route("/")
@login_required
def OrdensServico():
    tz = pytz.timezone('America/Fortaleza')
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM os JOIN clientes ON os.id_cliente = clientes.id JOIN mecanicos ON os.id_mecanico = mecanicos.id ORDER BY os.id ASC'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for valor in resultado:
            horaFortaleza = valor['criado_em'].astimezone(tz)
            valor['criado_em'] = horaFortaleza
            data = valor['criado_em'].strftime("%d/%m/%Y")
            valor['criado_em'] = data
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
@login_required
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
@login_required
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
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            for peca, quantidade in zip(pecas, quantidades):
                id_peca, nome, preco = peca.split('-')
                sql = 'SELECT quantidade FROM pecas WHERE id = %s'
                cursor.execute(sql, id_peca)
                estoque = cursor.fetchone()
                if estoque['quantidade'] == 0:
                    print('item sem estoque!!!')
                    flash('item sem estoque!!!', 'info')
                    return redirect(url_for('ordens.OrdensServico'))
                elif int(quantidade) <= estoque['quantidade']:
                    novaQtd = estoque['quantidade'] - int(quantidade)
                    sql = 'INSERT INTO itens_os (id_os, nome, quantidade, preco) VALUES (%s, %s, %s, %s)'
                    cursor.execute(sql, (id_os, nome, quantidade, preco))
                    sql = 'UPDATE pecas SET quantidade = %s WHERE id = %s'
                    cursor.execute(sql, (novaQtd, id_peca))
                    print('Adicionado com sucesso')
                else:
                    print('quantidade maior que o estoque!!!')
                    flash('quantidade maior que o estoque!!!', 'info')
                    return redirect(url_for('ordens.OrdensServico'))
            conexao.commit()
            flash('itens adicionados com sucesso!!!', 'success')
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

@ordens_bp.route("/info_os/<int:id_os>")
@login_required
def InfoOs(id_os):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM os JOIN clientes ON os.id_cliente = clientes.id JOIN mecanicos ON os.id_mecanico = mecanicos.id WHERE os.id = %s'
        cursor.execute(sql, id_os)
        cliente = cursor.fetchone()
        sql = 'SELECT id, nome, quantidade, preco FROM itens_os WHERE id_os = %s'
        cursor.execute(sql, id_os)
        itens_os = cursor.fetchall()
        novoItem = []
        soma = 0
        for item in itens_os:
            quantidade = int(item['quantidade'])
            preco = int(item['preco'])
            soma = soma + (quantidade * preco)
            item['quantidade'] = quantidade
            item['preco'] = preco
            item['valor'] = item['preco'] * item['quantidade']
            novoItem.append(item)
        return render_template("info_os.html", itens_os = novoItem, cliente = cliente, soma = soma)
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

@ordens_bp.route("/deletar_os/<int:id>")
@login_required
def DeletarOs(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM os WHERE id = %s'
        cursor.execute(sql, (id, ))
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

@ordens_bp.route("/deletar_item_os/<int:id>/<int:id_os>/<nome_peca>")
@login_required
def DeletarItemOs(id, id_os, nome_peca):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT quantidade FROM itens_os WHERE id = %s'
        cursor.execute(sql, id)
        quantidade = cursor.fetchone()
        sql = 'DELETE FROM itens_os WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        sql = 'SELECT quantidade FROM pecas WHERE nome = %s'
        cursor.execute(sql, nome_peca)
        resultado = cursor.fetchone()
        novaQtd = resultado['quantidade'] + int(quantidade['quantidade'])
        sql = 'UPDATE pecas SET quantidade = %s WHERE nome = %s'
        cursor.execute(sql, (novaQtd, nome_peca))
        conexao.commit()
        return redirect(url_for('ordens.InfoOs', id_os = id_os))
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