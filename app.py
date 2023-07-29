from flask import Flask
from admin.routes import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.register_blueprint(admin_bp, url_prefix='/admin')