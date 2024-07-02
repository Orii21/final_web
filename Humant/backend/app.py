from flask import Flask
from flask_cors import CORS
from models import mysql
from routes.user_routes import bp as user_bp
from routes.absensi_routes import bp as absensi_bp
from routes.jabatan_routes import bp as jabatan_bp
from routes.kritikan_routes import bp as kritikan_bp
from routes.gaji_routes import bp as gaji_bp

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
mysql.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(absensi_bp, url_prefix='/absensi')
app.register_blueprint(gaji_bp, url_prefix='/gaji')
app.register_blueprint(kritikan_bp, url_prefix='/kritikan')
app.register_blueprint(jabatan_bp, url_prefix='/jabatan')


if __name__ == '__main__':
    app.run(debug=True)
