from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_management.db'  # SQLite no mesmo diretório
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")  # Chave secreta para a aplicação
    db.init_app(app)