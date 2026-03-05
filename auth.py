from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_nome' not in session:
            flash("efetue o login primeiro!!!", "info")
            return redirect(url_for('usuarios.Login'))
        return f(*args, **kwargs)
    return wrapper