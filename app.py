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
    
@app.route("/painelServicos")
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
        
@app.route('/buscar_clientes')
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

@app.route("/cadastrar_clientes", methods = ['GET', 'POST'])
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
    
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route("/cadastrarveiculos", methods = ['GET', 'POST'])
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

@app.route("/buscar_veiculos")
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

@app.route("/cadastrarmecanicos")
def CadastrarMecanicos():
    return render_template("cadastrarmecanicos.html")

@app.route("/buscar_mecanicos")
def BuscarMecanicos():
    return render_template("mecanicos.html")

@app.route("/OS")
def CriarOs():
    return render_template("OS.html")
    
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