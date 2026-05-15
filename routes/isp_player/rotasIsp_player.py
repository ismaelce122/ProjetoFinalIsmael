from flask import render_template, Blueprint

ispPlayer_bp = Blueprint("ispPlayer", __name__, template_folder='ispPlayer_templates', static_folder='ispPlayer_static')

@ispPlayer_bp.route("/isp_player")
def ispPlayer():
    return render_template('isp_player.html')