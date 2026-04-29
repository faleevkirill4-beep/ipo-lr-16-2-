// static/js/main.js

// Функция получения CSRF-токена из cookie
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

// Показ уведомления (Bootstrap Alert)
function showNotification(message, type = 'success') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        // Создаем контейнер если его нет
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const containerFinal = document.getElementById('alert-container') || document.querySelector('#alert-container');
    containerFinal.appendChild(alertDiv);
    
    // Автоматически скрыть через 3 секунды
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => alertDiv.remove(), 300);
    }, 3000);
}

// Показ спиннера загрузки
function showSpinner(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-2">Загрузка товаров...</p>
            </div>
        `;
    }
}

// Функция загрузки товаров из API
async function loadProductsFromAPI() {
    const productsContainer = document.getElementById('products-container');
    if (!productsContainer) return;
    
    // Показываем спиннер
    showSpinner('products-container');
    
    try {
        const response = await fetch('/api/products/');
        
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        const products = await response.json();
        renderProducts(products, productsContainer);
        
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
        productsContainer.innerHTML = `
            <div class="alert alert-danger text-center" role="alert">
                <i class="bi bi-exclamation-triangle"></i> 
                Не удалось загрузить товары. Пожалуйста, обновите страницу.
            </div>
        `;
        showNotification('Ошибка загрузки товаров из API', 'danger');
    }
}

// Функция отрисовки товаров на странице
function renderProducts(products, container) {
    if (!products || products.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info text-center" role="alert">
                <i class="bi bi-info-circle"></i> 
                Товары не найдены.
            </div>
        `;
        return;
    }
    
    let html = '<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">';
    
    products.forEach(product => {
        const inStock = product.count > 0;
        const imageUrl = product.image || '';
        
        html += `
            <div class="col">
                <div class="card h-100 shadow-sm product-card" data-product-id="${product.id}">
                    <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                        ${imageUrl ? 
                            `<img src="${imageUrl}" class="img-fluid" alt="${product.name}" style="height: 100%; object-fit: cover;">` :
                            `<i class="bi bi-image" style="font-size: 48px; color: #ccc;"></i>`
                        }
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${escapeHtml(product.name)}</h5>
                        <p class="card-text text-primary h4">${product.price} ₽</p>
                        <p class="card-text small ${inStock ? 'text-success' : 'text-danger'}">
                            ${inStock ? `✓ В наличии: ${product.count} шт.` : '✗ Нет в наличии'}
                        </p>
                    </div>
                    <div class="card-footer bg-transparent border-0 pb-3">
                        <a href="/catalog/${product.id}/" class="btn btn-outline-primary w-100 mb-2">
                            <i class="bi bi-eye"></i> Подробнее
                        </a>
                        ${inStock ? `
                            <button class="btn btn-primary w-100 add-to-cart-btn" data-product-id="${product.id}" data-product-name="${escapeHtml(product.name)}">
                                <i class="bi bi-cart-plus"></i> В корзину
                            </button>
                        ` : `
                            <button class="btn btn-secondary w-100" disabled>
                                <i class="bi bi-cart-x"></i> Нет в наличии
                            </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Привязываем обработчики к кнопкам "В корзину"
    attachAddToCartHandlers();
}

// Функция добавления в корзину (POST на /api/basket/add/)
async function addToCart(productId, productName) {
    // Показываем индикацию на кнопке
    const button = document.querySelector(`.add-to-cart-btn[data-product-id="${productId}"]`);
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Добавление...';
    
    try {
        const response = await fetch('/api/basket/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                product_id: parseInt(productId),
                quantity: 1
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ошибка: ${response.status}`);
        }
        
        const data = await response.json();
        showNotification(`✅ ${productName} добавлен в корзину!`, 'success');
        
        // Обновляем счетчик корзины, если он есть на странице
        updateCartCounter();
        
    } catch (error) {
        console.error('Ошибка добавления в корзину:', error);
        showNotification(`❌ Не удалось добавить "${productName}" в корзину: ${error.message}`, 'danger');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

// Привязка обработчиков ко всем кнопкам "В корзину"
function attachAddToCartHandlers() {
    const buttons = document.querySelectorAll('.add-to-cart-btn');
    buttons.forEach(button => {
        button.removeEventListener('click', handleAddToCart);
        button.addEventListener('click', handleAddToCart);
    });
}

// Обработчик клика по кнопке "В корзину"
function handleAddToCart(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const productId = button.dataset.productId;
    const productName = button.dataset.productName;
    
    if (productId) {
        addToCart(productId, productName);
    }
}

// Обновление счетчика корзины в навбаре
async function updateCartCounter() {
    try {
        const response = await fetch('/api/basket/');
        if (response.ok) {
            const basket = await response.json();
            const totalItems = basket.total_items || 0;
            
            const cartBadge = document.querySelector('.cart-badge, .basket-count');
            if (cartBadge) {
                if (totalItems > 0) {
                    cartBadge.textContent = totalItems;
                    cartBadge.style.display = 'inline-block';
                } else {
                    cartBadge.style.display = 'none';
                }
            }
        }
    } catch (error) {
        console.error('Ошибка обновления счетчика корзины:', error);
    }
}

// Функция для экранирования HTML (защита от XSS)
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Загрузка товаров при загрузке страницы каталога
document.addEventListener('DOMContentLoaded', function() {
    // Если это страница каталога (есть контейнер для товаров)
    const productsContainer = document.getElementById('products-container');
    if (productsContainer && window.location.pathname === '/catalog/') {
        loadProductsFromAPI();
    }
});