from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'senhasecreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'  # Banco de dados SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Criar tabelas antes do primeiro request
    
    def create_tables():
        from .models import Cliente, Produto, Pedido, ItemPedido, Pagamento
        db.create_all()

    return app