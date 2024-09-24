let totalQuantity = 0; // Variável para armazenar a quantidade total de itens

// Função para atualizar o controle de quantidade de cada combo e produto
document.querySelectorAll('.combos_produtos div, .cardapio_produtos div, .premium_produtos div').forEach(item => {
    let quantity = 0;
    const decreaseButton = item.querySelector('.btn-decrease');
    const increaseButton = item.querySelector('.btn-increase');
    const quantityDisplay = item.querySelector('.quantity');
    const quantityInput = item.querySelector('input[type="hidden"]');

    // Garantir que cada botão tenha apenas um evento associado
    decreaseButton.removeEventListener('click', decreaseQuantity);
    decreaseButton.addEventListener('click', decreaseQuantity);
    
    increaseButton.removeEventListener('click', increaseQuantity);
    increaseButton.addEventListener('click', increaseQuantity);

    function decreaseQuantity() {
        if (quantity > 0) {
            quantity--;
            quantityDisplay.textContent = quantity;
            quantityInput.value = quantity; // Atualiza o input oculto
            totalQuantity--;
            updateCartCount();
        }
    }

    function increaseQuantity() {
        quantity++;
        quantityDisplay.textContent = quantity;
        quantityInput.value = quantity; // Atualiza o input oculto
        totalQuantity++;
        updateCartCount();
    }
});

// Função para atualizar o contador do carrinho
function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');

    if (totalQuantity > 0) {
        cartCountElement.style.display = 'flex'; // Exibe o contador se tiver itens
        cartCountElement.textContent = totalQuantity/2; // Atualiza o número
    } else {
        cartCountElement.style.display = 'none'; // Oculta se não tiver itens
    }
}

function changeQuantity(id, delta) {
    let quantitySpan = document.getElementById(id + '_quantity');
    let quantityInput = document.getElementById(id + '_quantidade');
    let quantity = parseInt(quantitySpan.textContent) + delta;
    if (quantity >= 0) {
        quantitySpan.textContent = quantity;
        quantityInput.value = quantity;
    }
}

function validateForm(event) {
    const combos = ['combo1', 'combo2', 'combo3']; // Adicione todos os IDs de combos aqui
    const produtos = ['produto1', 'produto2', 'produto3', 'produto4', 'produto5', 'produto6', 'produto7', 'produto8', 'produto9']; // Adicione todos os IDs de produtos aqui
    let hasSelectedItem = false;

    // Verifica se pelo menos um combo ou produto foi selecionado
    [...combos, ...produtos].forEach(item => {
        const quantity = parseInt(document.getElementById(item + '_quantidade').value);
        if (quantity > 0) {
            hasSelectedItem = true; // Pelo menos um item está selecionado
        }
    });

    if (!hasSelectedItem) {
        alert('Por favor, selecione pelo menos um item antes de realizar o pedido.');
        event.preventDefault(); // Impede o envio do formulário
        return false; // Não envia o formulário
    }

    return true; // Permite o envio do formulário
}

// Limpa as quantidades quando a página é carregada com GET
window.onload = function() {
    if (window.location.search) {
        const combos = ['combo1', 'combo2', 'combo3'];
        const produtos = ['produto1', 'produto2', 'produto3', 'produto4', 'produto5', 'produto6', 'produto7', 'produto8', 'produto9'];
        [...combos, ...produtos].forEach(item => {
            document.getElementById(item + '_quantidade').value = 0;
            document.getElementById(item + '_quantity').textContent = 0;
        });
    }
};
