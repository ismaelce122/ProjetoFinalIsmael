from flask import Flask, render_template, session, redirect, url_for
from routes import Registrar_Blueprints
from auth import login_required
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
Registrar_Blueprints(app)

@app.route("/")
@login_required
def index():
    return redirect(url_for('PainelServicos'))
    
@app.route("/painel")
@login_required
def PainelServicos():
    return render_template('painelServicos.html', session = session)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuarios.Login'))
    
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