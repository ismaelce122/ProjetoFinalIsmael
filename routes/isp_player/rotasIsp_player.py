from flask import render_template, Blueprint, request, Response
import requests

ispPlayer_bp = Blueprint("ispPlayer", __name__, template_folder='ispPlayer_templates', static_folder='ispPlayer_static')

@ispPlayer_bp.route("/isp_player")
def ispPlayer():
    return render_template('isp_player.html')

@ispPlayer_bp.route("/isp_player/politica-privacidade")
def politicaPortugues():
    return render_template('politica_portugues.html')

@ispPlayer_bp.route("/isp_player/privacy-policy-en")
def politicaIngles():
    return render_template('politica_ingles.html')

@ispPlayer_bp.route("/isp_player/privacy-policy-ko")
def politicaKoreano():
    return render_template('politica_koreano.html')

@ispPlayer_bp.route("/isp_player/proxy")
def Proxy():
    url = request.args.get("url")
    if not url:
        return {"error": "URL não fornecida"}, 400

    # Faz a requisição ao servidor IPTV
    resp = requests.get(url)

    # Cria resposta com os dados recebidos
    response = Response(resp.content, status=resp.status_code)

    # Adiciona cabeçalhos CORS para liberar no navegador
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    return response
