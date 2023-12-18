import os
from flask import Flask 

from .extensions import api, db, jwt
from .resources import ns
from .models import User

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/db_minatku"
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