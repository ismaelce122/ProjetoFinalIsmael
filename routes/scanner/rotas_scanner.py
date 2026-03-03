from flask import render_template, Blueprint
from auth import login_required

scanner_bp = Blueprint("scanner", __name__, template_folder='scanner_templates', static_folder='scanner_static')

@scanner_bp.route('/scanner')
@login_required
def Scan():
    return render_template('scan.html')