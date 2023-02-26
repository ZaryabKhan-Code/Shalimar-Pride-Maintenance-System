from flask import *
from config.config import *
from util.resident_util import *
resident_dashboard_router  = Blueprint('dashboard_model',__name__,static_folder='static', template_folder='view/template')

@resident_dashboard_router.route('/route_name')
@login_required
def resident_dashboard_route():
    return current_user.resident_name