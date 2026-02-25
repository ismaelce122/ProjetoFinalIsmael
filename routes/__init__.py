from .usuarios import usuarios_bp
from .mecanicos import mecanicos_bp
from .veiculos import veiculos_bp
from .estoque import estoque_bp
from .ordens_de_servico import ordens_bp

def Registrar_Blueprints(app):
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(mecanicos_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(ordens_bp)