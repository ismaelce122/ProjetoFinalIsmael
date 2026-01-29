from flask import Flask, render_template, session, redirect, url_for, request
import pymysql as my
from dotenv import load_dotenv
from datetime import datetime
import pytz
import os
import bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

tz = pytz.timezone('America/Sao_Paulo')
hora = datetime.now(tz)

def ConectarBanco():
    conexao = my.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        cursorclass = my.cursors.DictCursor 
    )
    return conexao

@app.route("/")
def index():
    if session:
        return redirect(url_for('PainelServicos'))
    else:
        return render_template('login.html')

@app.route("/painelServicos")
def PainelServicos():
    if session:
        return render_template('painelServicos.html', session = session)
    else:
        return render_template('login.html')
    
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
            conexao = ConectarBanco()
            cursor = conexao.cursor()
            sql = 'INSERT INTO clientes (nome, telefone, email, documento, endereco, senha, criado_em) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (cliente['nome'], cliente['telefone'], cliente['email'], cliente['documento'], cliente['endereco'], cliente['senhaHash'], hora))
            conexao.commit()
            conexao.close()
            cadastrou = True
            return redirect(url_for('PainelServicos', cadastrou = cadastrou))
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
        conexao = ConectarBanco()
        cursor = conexao.cursor()
        sql = 'SELECT * FROM clientes WHERE email= %s'
        cursor.execute(sql, (email, ))
        usuario = cursor.fetchone()
        if usuario:
            senhaHash = usuario['senha']
            print(f'Usuário Logado: {usuario['nome']}')
            if bcrypt.checkpw(senha.encode('utf-8'), senhaHash.encode('utf-8')):
                session['usuario_nome'] = usuario['nome']
                session['usuario_id'] = usuario['id']
                return redirect(url_for('PainelServicos'))
            else:
                print('Senha Incorreta!!!')
                return redirect(url_for('Login'))
            
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Login'))

if __name__ == "__main__":
    app.run(debug=True)