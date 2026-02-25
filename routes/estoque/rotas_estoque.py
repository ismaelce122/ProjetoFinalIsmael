from flask import render_template, redirect, request, url_for, Blueprint
from config import banco as db
import pymysql

estoque_bp = Blueprint("estoque", __name__, url_prefix='/estoque', template_folder='estoque_templates', static_folder='estoque_static')

@estoque_bp.route("/")
def Estoque():
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM pecas ORDER BY nome ASC'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("estoque.html", resultado = resultado)
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

@estoque_bp.route("/cadastrar_categoria", methods = ['GET', 'POST'])
def CadastrarCategoria():
    if request.method == 'GET':
        return render_template("cadastrar_categoria.html")
    elif request.method == 'POST':
        categoria = request.form.get('nome')
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO categoria (nome) VALUES (%s)'
            cursor.execute(sql, (categoria, ))
            conexao.commit()
            return redirect(url_for('estoque.Estoque'))
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

@estoque_bp.route("/cadastrar_subcategoria", methods = ['GET', 'POST'])
def CadastrarSubcategoria():
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM categoria ORDER BY nome ASC'
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return render_template("cadastrar_subcategoria.html", resultado = resultado)
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
        sub_categoria = {
            'nome': request.form.get('nome'),
            'id_categoria': request.form.get('id_categoria')
        }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO subcategoria (nome, id_categoria) VALUES (%s, %s)'
            cursor.execute(sql, (sub_categoria['nome'], sub_categoria['id_categoria']))
            conexao.commit()
            return redirect(url_for('estoque.Estoque'))
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

@estoque_bp.route("/cadastrar_peca", methods = ['GET', 'POST'])
def CadastrarPeca():
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM subcategoria ORDER BY nome ASC'
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return render_template("cadastrar_peca.html", resultado = resultado)
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
        peca = {
                'nome': request.form.get('nome'),
                'quantidade': request.form.get('quantidade'), 
                'preco': request.form.get('preco'),
                'localizacao': request.form.get('localizacao'),
                'id_subcategoria': request.form.get('id_subcategoria')
            }
        if peca['localizacao'] == '' or peca['localizacao'] == None:
            peca['localizacao'] = 'Localização a ser Definida'
        if peca['quantidade'] == '' or peca['quantidade'] == None:
            peca['quantidade'] = str('Sem Estoque')
        if peca['preco'] == '' or peca['preco'] == None:
            peca['preco'] = 'Preço Indefinido'
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO pecas (nome, quantidade, preco, localizacao, id_subcategoria) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (peca['nome'], peca['quantidade'], peca['preco'], peca['localizacao'], peca['id_subcategoria']))
            conexao.commit()
            return redirect(url_for('estoque.Estoque'))
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

@estoque_bp.route("/editar_peca/<int:id>/<int:id_subcategoria>", methods = ['GET', 'POST'])
def EditarPeca(id, id_subcategoria):
    if request.method == 'GET':
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'SELECT * FROM subcategoria WHERE id = %s'
            cursor.execute(sql, (id_subcategoria, ))
            idSubcategoria = cursor.fetchone()
            sql = 'SELECT * FROM pecas WHERE id = %s'
            cursor.execute(sql, (id, ))
            pecas = cursor.fetchone()
            sql = 'SELECT * FROM subcategoria WHERE id <> %s ORDER BY nome ASC'
            cursor.execute(sql, (id_subcategoria, ))
            subcategoria = cursor.fetchall()
            return render_template('editar_pecas.html', subcategoria = subcategoria, pecas = pecas, idSubcategoria = idSubcategoria)
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
        peca = {
                'nome': request.form.get('nome'),
                'quantidade': request.form.get('quantidade'), 
                'preco': request.form.get('preco'),
                'localizacao': request.form.get('localizacao'),
                'id_subcategoria': request.form.get('id_subcategoria')
            }
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'UPDATE pecas SET nome = %s, quantidade = %s, preco = %s, localizacao = %s, id_subcategoria = %s WHERE id = %s'
            cursor.execute(sql, (peca['nome'], peca['quantidade'], peca['preco'], peca['localizacao'], peca['id_subcategoria'], id))
            conexao.commit()
            return redirect(url_for('estoque.Estoque'))
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

@estoque_bp.route("/deletar_peca/<int:id>")
def DeletarPeca(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM pecas WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('estoque.Estoque'))
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