from flask import *
from config.config import *
from router.resident_router import *

app = Flask(__name__, static_folder='static', template_folder='view/template')
init_app(app)

app.register_blueprint(resident_router)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)