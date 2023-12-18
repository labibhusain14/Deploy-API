import os
from flask import Flask 

from .extensions import api, db, jwt
from .resources import ns
from .models import User

def create_app():
    app = Flask(__name__)

    # Menggunakan public IP address dan connection name yang disediakan
    db_config = {
        'user': 'root',
        'password': 'minatkuapp',  # Masukkan password database Anda di sini
        'db': 'db_minatku',
        'host': '34.128.74.245',
        'unix_socket': '/cloudsql/deploy-api-408210:asia-southeast2:minatkudb'
    }

    # Mengonfigurasi SQLAlchemy untuk menggunakan MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['db']}?unix_socket={db_config['unix_socket']}"

    app.config["JWT_SECRET_KEY"] = "thisisasecret"
  
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.add_namespace(ns)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email=identity).first()
        
    return app

if __name__ == "__main__":
    # Menentukan port aplikasi
    port = int(os.environ.get("PORT", 8080))  # Ganti 8080 dengan port yang diinginkan
    app = create_app()
    app.run(host='0.0.0.0', port=port)
