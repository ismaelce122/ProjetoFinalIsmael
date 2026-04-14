from flask import render_template, Blueprint

iptv_bp = Blueprint("iptv", __name__, template_folder='iptv_templates', static_folder='iptv_static')

@iptv_bp.route("/iptv")
def Iptv():
    return render_template('isp_iptv.html')