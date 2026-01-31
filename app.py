from flask import Flask, render_template, session, redirect, url_for, request, make_response
from datetime import datetime
from config import banco as db
import pymysql
import pytz
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

tz = pytz.timezone('America/Sao_Paulo')
hora = datetime.now(tz)

@app.route("/")
def index():
    if 'usuario' not in session:
        return redirect(url_for('Login'))
    else:
        return redirect(url_for('PainelServicos'))

@app.route("/painelServicos")
def PainelServicos():
    if 'usuario' not in session:
        return redirect(url_for('Login')):
    else:
        return render_template('painelServicos.html', session = session)
    
@app.route("/cadastrarcliente", methods = ['GET', 'POST'])
def CadastrarCliente():
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
        cadastrou = False
        try:
            conexao = db.ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO clientes (nome, telefone, email, documento, endereco, senha, criado_em) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (cliente['nome'], cliente['telefone'], cliente['email'], cliente['documento'], cliente['endereco'], cliente['senhaHash'], hora))
            conexao.commit()
            conexao.close()
            cadastrou = True
            return redirect(url_for('PainelServicos', cadastrou = cadastrou))
        except pymysql.MySQLError as e:
            print('-----------------------------------------------')
            print(f'Erro no banco de dados: {e.args[0]}')
            print(f'Mensagem do Erro: {e.args[1]}')
            print('-----------------------------------------------')
            return f'<h2>Erro no banco de dados: {e}</h2>'
        except Exception as e:
            erro = True
            print(f'Houve um erro: {e}')
            return render_template('login.html') 

@app.route("/cadastrarmecanicos")
def CadastrarMecanicos():
    return render_template("cadastrarmecanicos.html")

@app.route("/OS")
def CriarOs():
    return render_template("OS.html")

@app.route("/cadastrarveiculos")
def CadastrarVeiculos():
    return render_template("cadastrarveiculos.html")

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
            conexao.close()
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
                            <h2>Senha Incorreta!!!</h2>
                            <a href="/login"><<< Voltar ao Login</a>
                           ''' 
            else:
                print('E-mail Incorreto!!!')
                return '''
                        <h2>E-mail Incorreto!!!</h2>
                        <a href="/login"><<< Voltar ao Login</a>
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
            
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')
    
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True)
