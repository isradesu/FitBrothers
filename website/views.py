from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Pedido, ItemPedido, Produto, Cliente, Pagamento
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/pagamento', methods=['GET', 'POST'])
def pagamento():
    if request.method == 'GET':
        # Carregar os itens do pedido da sessão se estiverem presentes
        itens = session.get('itens_pedido', [])
        return render_template("pagamento.html", itens_pedido=itens)

    if request.method == 'POST':
        # Adiciona cada combo e produto ao pedido se a quantidade for maior que zero
        itens = []
        combos = ['combo1', 'combo2', 'combo3']
        produtos = ['produto1', 'produto2', 'produto3', 'produto4', 'produto5', 'produto6', 'produto7', 'produto8', 'produto9']

        # Coletar itens dos combos
        for combo in combos:
            quantidade = int(request.form.get(f'{combo}_quantidade', 0))
            nome = request.form.get(f'{combo}_nome', '')
            preco = float(request.form.get(f'{combo}_preco', 0.0))
            if quantidade > 0:
                itens.append({'nome': nome, 'quantidade': quantidade, 'preco': preco})

        # Coletar itens dos produtos
        for produto in produtos:
            quantidade = int(request.form.get(f'{produto}_quantidade', 0))
            nome = request.form.get(f'{produto}_nome', '')
            preco = float(request.form.get(f'{produto}_preco', 0.0))
            if quantidade > 0:
                itens.append({'nome': nome, 'quantidade': quantidade, 'preco': preco})

        # Salvar itens na sessão
        if itens:
            session['itens_pedido'] = itens
            session.modified = True

        # Coletar dados do cliente e do pagamento
        cliente_nome = request.form.get('nome')
        cliente_telefone = request.form.get('telefone')
        cliente_endereco = request.form.get('endereco')
        cliente_numero = request.form.get('numero')
        cliente_bairro = request.form.get('bairro')
        cliente_complemento = request.form.get('complemento')
        metodo_pagamento = request.form.get('pagamento')

        # Adicionar pedido ao banco de dados
        if cliente_nome and cliente_telefone and cliente_endereco:
            adicionar_pedido(cliente_nome, cliente_telefone, cliente_endereco,
                             cliente_numero, cliente_bairro, cliente_complemento,
                             metodo_pagamento, itens)

            # Opcional: Mensagem de sucesso
            success_message = "Pedido realizado com sucesso!"
            return render_template("pagamento.html", itens_pedido=itens, success=success_message)

        # Se os dados do cliente não estiverem completos, renderizar a página novamente
        return render_template("pagamento.html", itens_pedido=itens, error="Preencha todos os campos obrigatórios.")

   
    return render_template("pagamento.html", itens_pedido=session.get('itens_pedido', []))

def adicionar_pedido(cliente_nome, cliente_telefone, cliente_endereco, cliente_numero,
                     cliente_bairro, cliente_complemento, metodo_pagamento, itens):
    # Criar um novo cliente
    novo_cliente = Cliente(
        nome=cliente_nome,
        telefone=cliente_telefone,
        endereco=cliente_endereco,
        numero=cliente_numero,
        bairro=cliente_bairro,
        complemento=cliente_complemento
    )
    db.session.add(novo_cliente)
    db.session.commit()  # Salvar cliente no banco

    # Criar o método de pagamento
    pagamento_novo = Pagamento(metodo_pagamento=metodo_pagamento, valor_total=0)  # Ajuste o valor_total conforme necessário
    db.session.add(pagamento_novo)
    db.session.commit()

    # Criar um novo pedido
    novo_pedido = Pedido(cliente_id=novo_cliente.id, data=datetime.utcnow(), pagamento_id=pagamento_novo.id)
    db.session.add(novo_pedido)

    # Adicionar os itens do pedido
    for item in itens:
        produto = Produto.query.filter_by(nome=item['nome']).first()
        if produto:
            item_pedido = ItemPedido(pedido_id=novo_pedido.id, produto_id=produto.id, quantidade=item['quantidade'])
            db.session.add(item_pedido)

    # Salvar tudo no banco de dados
    db.session.commit()
