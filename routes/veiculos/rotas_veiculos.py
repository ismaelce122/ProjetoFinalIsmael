from flask import render_template, redirect, request, url_for, Blueprint
from config import banco as db
import pymysql

veiculos_bp = Blueprint("veiculos", __name__, url_prefix='/veiculos', template_folder='veiculos_templates', static_folder='veiculos_static')

@veiculos_bp.route("/")
def BuscarVeiculos():
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM veiculos JOIN clientes ON veiculos.id_cliente = clientes.id ORDER BY nome'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template('veiculos.html', resultado = resultado)
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

@veiculos_bp.route("/cadastrar", methods = ['GET', 'POST'])
def CadastrarVeiculos():
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM clientes ORDER BY nome ASC'
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return render_template('cadastrarveiculos.html', resultado = resultado)
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
        veiculo = {
                'id_cliente': request.form.get('id_cliente'),
                'modelo': request.form.get('modelo'), 
                'marca': request.form.get('marca'),
                'ano': request.form.get('ano'),
                'placa': request.form.get('placa'),   
                'observacoes': request.form.get('observacoes')
            }
        if veiculo['observacoes'] == '' or veiculo['observacoes'] == None:
            veiculo['observacoes'] = 'Sem Observações'
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO veiculos (id_cliente, modelo, marca, ano, placa, observacoes) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (veiculo['id_cliente'], veiculo['modelo'], veiculo['marca'], veiculo['ano'], veiculo['placa'], veiculo['observacoes']))
            conexao.commit()
            return redirect(url_for('veiculos.BuscarVeiculos'))
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

@veiculos_bp.route("/editar/<int:id>", methods = ['GET', 'POST'])
def EditarVeiculo(id):
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM veiculos WHERE id = %s'
            cursor.execute(sql, (id, ))
            resultado = cursor.fetchone()
            return render_template('editar_veiculos.html', resultado = resultado)
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
        veiculo = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'), 
                'ano': request.form.get('ano'),
                'placa': request.form.get('placa'),
                'observacoes': request.form.get('observacoes')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'UPDATE veiculos SET marca = %s, modelo = %s, ano = %s, placa=%s, observacoes=%s WHERE id = %s'
            cursor.execute(sql, (veiculo['marca'], veiculo['modelo'], veiculo['ano'], veiculo['placa'], veiculo['observacoes'], id))
            conexao.commit()
            return redirect(url_for('veiculos.BuscarVeiculos'))
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

@veiculos_bp.route("/deletar/<int:id>")
def DeletarVeiculo(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM veiculos WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('veiculos.BuscarVeiculos'))
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