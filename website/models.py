from . import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    itens_pedido = db.relationship('ItemPedido', backref='produto', lazy=True)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    pagamento_id = db.Column(db.Integer, db.ForeignKey('pagamento.id'), nullable=False)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    pedidos = db.relationship('Pedido', backref='pagamento', lazy=True)