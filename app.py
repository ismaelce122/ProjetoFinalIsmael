from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")





@app.route("/cadastrarveiculos")
def CadastrarVeiculos():
    return render_template("cadastrarveiculos.html")

# Executa o servidor SOMENTE localmente
if __name__ == "__main__":
    app.run(debug=True)