from flask import Flask, render_template, request
import mysql.connector as my
import bcrypt

app = Flask(__name__)

def conectar():
    conexao = my.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'sistema_os'
    )
    return conexao

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrarcliente")
def CadastrarCliente():
    return render_template("cadastrarcliente.html")

@app.route("/cadastrarmecanicos")
def CadastrarMecanicos():
    return render_template("cadastrarmecanicos.html")

@app.route("/OS")
def CriarOs():
    return render_template("OS.html")

@app.route("/cadastrarveiculos")
def CadastrarVeiculos():
    return render_template("cadastrarveiculos.html")

@app.route("/login")
def Login():
    return render_template("login.html")

# Executa o servidor SOMENTE localmente
if __name__ == "__main__":
    app.run(debug=True)