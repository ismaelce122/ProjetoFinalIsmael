from flask import Flask, render_template, session, redirect, url_for, request
from config import banco as db
import pymysql
import pytz
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    if session:
        return redirect(url_for('PainelServicos'))
    return redirect(url_for('Login'))
    
@app.route("/painel")
def PainelServicos():
    if session:
        return render_template('painelServicos.html', session = session)
    return redirect(url_for('Login'))
    
@app.route("/usuario", methods = ['GET', 'POST'])
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
            return redirect(url_for('Login'))
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
        
@app.route('/clientes')
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

@app.route("/login", methods = ['GET', 'POST'])
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

@app.route("/clientes/cadastrar", methods = ['GET', 'POST'])
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
            return redirect(url_for('BuscarClientes'))
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

@app.route("/clientes/editar/<int:id>", methods = ['GET', 'POST'])
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
            return redirect(url_for('BuscarClientes'))
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

@app.route("/clientes/deletar/<int:id>")
def DeletarCliente(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM clientes WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('BuscarClientes'))
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
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route("/veiculos")
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

@app.route("/veiculos/cadastrar", methods = ['GET', 'POST'])
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
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO veiculos (id_cliente, modelo, marca, ano, placa, observacoes) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (veiculo['id_cliente'], veiculo['modelo'], veiculo['marca'], veiculo['ano'], veiculo['placa'], veiculo['observacoes']))
            conexao.commit()
            return redirect(url_for('BuscarVeiculos'))
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

@app.route("/veiculos/editar/<int:id>", methods = ['GET', 'POST'])
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
            return redirect(url_for('BuscarVeiculos'))
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

@app.route("/veiculos/deletar/<int:id>")
def DeletarVeiculo(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM veiculos WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('BuscarVeiculos'))
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

@app.route("/mecanicos")
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

@app.route("/mecanicos/cadastrar", methods = ['GET', 'POST'])
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
            return redirect(url_for('BuscarMecanicos'))
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

@app.route("/mecanicos/editar/<int:id>", methods = ['GET', 'POST'])
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
            return redirect(url_for('BuscarMecanicos'))
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

@app.route("/mecanicos/deletar/<int:id>")
def DeletarMecanico(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM mecanicos WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('BuscarMecanicos'))
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

@app.route("/ordens_de_servico")
def CriarOs():
    return render_template("OS.html")

@app.route("/ordens_de_servico/criar_ordem", methods = ['GET', 'POST'])
def CadastrarOs():
    if request.method == 'GET':
        return render_template("cadastrar_os.html")
    elif request.method == 'POST':
        pass

@app.route("/estoque")
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

@app.route("/estoque/cadastrar_categoria", methods = ['GET', 'POST'])
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
            return redirect(url_for('Estoque'))
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

@app.route("/estoque/cadastrar_subcategoria", methods = ['GET', 'POST'])
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
            return redirect(url_for('Estoque'))
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

@app.route("/estoque/cadastrar_peca", methods = ['GET', 'POST'])
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
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO pecas (nome, quantidade, preco, localizacao, id_subcategoria) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (peca['nome'], peca['quantidade'], peca['preco'], peca['localizacao'], peca['id_subcategoria']))
            conexao.commit()
            return redirect(url_for('Estoque'))
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

@app.route("/estoque/editar_peca/<int:id>/<int:id_subcategoria>", methods = ['GET', 'POST'])
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
            return redirect(url_for('Estoque'))
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

@app.route("/estoque/deletar_peca/<int:id>")
def DeletarPeca(id):
    try:
        conexao = db.ConectarBanco()
        cursor = conexao.cursor()
        sql = 'DELETE FROM pecas WHERE id = %s'
        cursor.execute(sql, (id, ))
        conexao.commit()
        return redirect(url_for('Estoque'))
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
    
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)