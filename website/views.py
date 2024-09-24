from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Pedido, ItemPedido, Produto
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/pagamento', methods=['GET', 'POST'])
def pagamento():
    if request.method == 'GET':
        pass  # Não é necessário limpar a sessão aqui

    if request.method == 'POST':
        # Adiciona cada combo e produto ao pedido se a quantidade for maior que zero
        itens = []
        combos = ['combo1', 'combo2', 'combo3']
        produtos = ['produto1', 'produto2', 'produto3', 'produto4', 'produto5', 'produto6', 'produto7', 'produto8', 'produto9']
        
        for combo in combos:
            quantidade = int(request.form.get(f'{combo}_quantidade', 0))
            nome = request.form.get(f'{combo}_nome', '')
            preco = float(request.form.get(f'{combo}_preco', 0.0))
            if quantidade > 0:
                itens.append({'nome': nome, 'quantidade': quantidade, 'preco': preco})
        
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

        return redirect(url_for('views.pagamento'))

    # Renderizar a mesma página com o resumo do pedido
    return render_template("pagamento.html", itens_pedido=session.get('itens_pedido', []))
