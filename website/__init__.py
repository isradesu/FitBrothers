from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'senhasecreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Criar tabelas antes do primeiro request
    
    from .models import Cliente, Produto, Pedido, ItemPedido, Pagamento
    
    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):  # Verifica se o banco de dados existe
        with app.app_context():  # Cria um contexto de aplicativo
            db.create_all()  # Cria todas as tabelas
        print('Banco Criado')
