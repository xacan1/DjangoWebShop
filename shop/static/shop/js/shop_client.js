"use strict";


const formatter = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const formatter0 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

window.addEventListener('load', update_cart_header());
window.addEventListener('load', update_wishlist_header());
window.addEventListener('load', setEventListener());
window.addEventListener('load', load_saved_values());
window.addEventListener('load', elements_listener());



async function elements_listener() {
    let selectSorting = document.getElementById('selectSorting');

    if (selectSorting) {
        selectSorting.addEventListener('change', sort_products);
    }
}

function load_saved_values() {
    let selectSorting = document.getElementById('selectSorting');

    if (selectSorting) {
        selectSorting.value = get_selectSorting(selectSorting);
    }
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setEventListener() {
    let modal = document.getElementById('successAddProductToCartModal');

    if (modal) {
        modal.addEventListener('show.bs.modal', function (event) {
            handlerAddProductToCart(event);
        });
    }
}

async function get_cart_info() {
    // не авторизованным пользователям сервер ничего не вернет по этому запоним объект по умолчанию
    let cart_info = {};
    cart_info.quantity = 0;
    cart_info.amount = 0;
    cart_info.products = [];

    let options = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin'
    }

    let response = await fetch('/api/v1/get_cart_info', options);

    if (!response.ok && response.status != 401) {
        console.log('Ошибка HTTP: ' + response.status);
        return cart_info;
    }

    // не авторизованным пользователям сервер ничего не вернет
    if (response.status == 401) {
        return cart_info;
    }

    cart_info = await response.json();

    return cart_info;
}

// БЛОК РАБОТЫ С КОРЗИНОЙ В ШАПКЕ САЙТА

// Очищает корзину в заголовке сайта
function clear_cart_header() {
    let shop_cart = document.getElementById('shop-cart-header');
    let elements = shop_cart.querySelectorAll('.shop-for-del');

    for (let element of elements) {
        element.remove();
    }

    // подвал очистим, а не удалим
    let bottom = document.querySelector('.cart-items>.shopping-item>.bottom');

    if (bottom) {
        bottom.textContent = '';
    }
}

// Обновляет корзину на фронте ajax-запросом, перерисовывает ее заново каждый раз
async function update_cart_header() {
    let cart_header = document.querySelector('#shop-cart-header'); // отправная точка корзины в заголовке
    let cart_info = await get_cart_info();
    clear_cart_header();

    let product_list = cart_header.querySelector('.shopping-item>ul.shopping-list');
    let product_summary = cart_header.querySelector('#shop-total-quantity-cart');
    product_summary.textContent = 'Товаров: ' + formatter0.format(cart_info.quantity);

    for (let row of cart_info.products) {
        // добавим строки товара в DOM
        let new_li = document.createElement('li');
        new_li.className = 'shop-for-del';
        new_li.setAttribute('data-shop-product_cart-pk', row.id);

        // подправим путь к карточке товара
        let path_product = '/product-details/' + row.product.slug;

        new_li.innerHTML = `<div>\
            <a href="javascript:void(0)" onclick="delete_cart_product(this);" class="remove" title="Удалить товар"><i\
                    class="lni lni-close"></i></a>\
            <div class="cart-img-head">\
                <a class="cart-img" href="${path_product}"><img src="${row.product.photo}" alt="#"></a>\
            </div>\
        </div>\
        <div class="content">\
            <h4><a href="${path_product}">${row.product.name}</a></h4>\
            <p class="quantity">${formatter0.format(row.quantity)}x - <span class="amount">${formatter.format(row.amount)}</span></p>\
        </div>`;
        product_list.append(new_li);
    }

    // Заполним секцию Итог
    let bottom = cart_header.querySelector('.shopping-item>.bottom');

    bottom.innerHTML = `<div class="bottom">\
        <div class="total">\
            <span>Итого</span>\
            <span class="total-amount">${formatter.format(cart_info.amount)}</span>\
        </div>\
        <div class="button" hidden=false>\
            <a href="${document.domain}/checkout" class="btn animate">Оформить заказ</a>\
        </div>\
    </div>`;

    if (!cart_info.products) {
        let button = cart_header.querySelector('.shopping-item>.bottom>.button');
        button.setAttribute('hidden', true);
    }

    // обновим иконку коризны
    cart_header.querySelector('#shop-total-items').textContent = formatter0.format(cart_info.quantity);

    // если мы на странице корзины, то обновим и основную корзину
    if (document.querySelector('#shop-cart')) {
        update_cart(cart_info);
    }
}

// data-shop-product_cart-pk - это pk строки в корзине-заказе в БД сайта
async function delete_cart_product(btn) {
    const row = btn.parentElement.parentElement;
    const product_cart_pk = row.getAttribute('data-shop-product_cart-pk');

    let options = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin'
    }

    let response = await fetch(`/api/v1/carts/product_to_cart_delete/${product_cart_pk}`, options);

    if (!response.ok) {
        console.log('Ошибка HTTP: ' + response.status);
        return;
    }

    clear_cart_header();
    await update_cart_header();
}

// Возможно не пригодится функция , так как подобные вещи можно сделать через Django Forms и Messages
function get_selected_warehouse() {
    const selected_warehouse = 0;
    const radiobutton_checked = document.querySelector('input[name="warehouse"]:checked');

    // Если ни одна радио кнопка не выбрана, то подсветим выбор всех складов красным цветом
    if (!radiobutton_checked) {
        let warehouses = document.getElementsByClassName('warehouses')[0];

        if (warehouses) {
            warehouses.setAttribute('style', 'color: red');
            return selected_warehouse;
        }
    }

    selected_warehouse = radiobutton_checked.value;

    return selected_warehouse;
}

async function handlerAddProductToCart(event) {
    // Кнопка, запускающая модальное окно
    let button = event.relatedTarget;
    // При необходимости вы можете инициировать запрос AJAX здесь
    // а затем выполните обновление в обратном вызове.
    let result = await add_product_to_cart(button);

    // Обновите содержимое модального окна.
    let modalCheckSuccess = document.getElementById('shopCheckSuccess');
    let modalCheckPart1 = document.getElementById('shop-check-part-1');
    let modalCheckPart2 = document.getElementById('shop-check-part-2');
    let modalCheckDecliane = document.getElementById('shopCheckDecliane');
    let modalBody = document.querySelector('.modal-body>h6');

    if ('error' in result) {
        modalBody.textContent = 'Товар закончился на складе';
        modalCheckSuccess.className = '';
        modalCheckPart1.className = '';
        modalCheckPart2.className = '';
        modalCheckDecliane.className = 'shop-check-decline';
    }
    else {
        modalBody.textContent = 'Товар добавлен в корзину';
        modalCheckSuccess.className = 'shop-check-success';
        modalCheckPart1.className = 'shop-check-sign-success';
        modalCheckPart2.className = 'shop-check-sign-success';
        modalCheckDecliane.className = '';
    }
}

async function add_product_to_cart(btn) {
    const product_pk = btn.getAttribute('data-shop-product-pk');

    let data_product = {
        product_pk: product_pk,
        quantity: 1
    };

    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(data_product)
    };

    let response = await fetch('/api/v1/update_product_to_cart', options);

    if (!response.ok) {
        console.log('Ошибка HTTP add_product_to_cart: ' + response.status);
        return;
    }

    let result = await response.json();

    clear_cart_header();
    await update_cart_header();

    return result;
}

// КОНЕЦ БЛОКА РАБОТЫ С КОРЗИНОЙ ШАПКИ САЙТА

// БЛОК РАБОТЫ С КОРЗИНОЙ НА ОТДЕЛЬНОЙ СТРАНИЦЕ

// Очищает основную корзину
function clear_cart() {
    let total_amount_cart = document.getElementById('shop-cart');
    let elements = total_amount_cart.querySelectorAll('.shop-for-del');

    for (let element of elements) {
        element.remove();
    }
}

// после изменения количества
async function after_change_quantity(input) {
    // let price = row_price.textContent.replace(/[^\d.,]/g, '');
    const row = input.parentElement.parentElement.parentElement;
    // const product_cart_pk = row.getAttribute('data-shop-product_cart-pk');
    const product_pk = row.getAttribute('data-shop-product-pk');

    let data_cart_product = {
        product_pk: product_pk,
        quantity: parseFloat(input.value),
        set_new_quantity: true
    };

    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(data_cart_product)
    }

    // let response = await fetch(`/api/v1/carts/product_to_cart_update/${product_cart_pk}`, options);
    let response = await fetch('/api/v1/update_product_to_cart', options);

    if (!response.ok) {
        console.log('Ошибка HTTP after_change_quantity: ' + response.status);
        return;
    }

    clear_cart_header();
    await update_cart_header();
}

function update_cart(cart_info) {
    let cart_header = document.querySelector('#shop-cart'); // отправная точка корзины
    clear_cart();

    let product_list = cart_header.querySelector('#shop-cart>.cart-list-head');
    // добавим шапку таблицы
    if (cart_info.quantity > 0) {
        document.querySelector('#empty-cart').textContent = '';

        let cart_list_title = document.createElement('div');
        cart_list_title.className = 'cart-list-title shop-for-del';
        cart_list_title.innerHTML = `<div class="row">\
            <div class="col-lg-1 col-md-1 col-12">\
            </div>\
            <div class="col-lg-4 col-md-3 col-12">\
                <p>Товар</p>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12">\
                <p>Количество</p>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12">\
                <p>Сумма</p>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12" ${cart_info.discount > 0 ? '' : 'hidden'}>\
                <p>Скидка</p>\
            </div>\
            <div class="col-lg-1 col-md-2 col-12">\
                <p>Удалить</p>\
            </div>\
        </div>`;
        product_list.append(cart_list_title);
    }
    else {
        document.querySelector('#empty-cart').textContent = 'Корзина пуста, но это легко исправить ;)';
    }

    for (let row of cart_info.products) {
        let path_product = '/product-details/' + row.product.slug;
        let row_cart_order = document.createElement('div');
        row_cart_order.className = 'cart-single-list shop-for-del';
        row_cart_order.innerHTML = `<div class="row align-items-center shop-row-cart-order" data-shop-product_cart-pk="${row.id}" data-shop-product-pk="${row.product.pk}" data-shop-price="${row.price}">\
            <div class="col-lg-1 col-md-1 col-12">\
                <a href="${path_product}"><img src="${row.product.photo ? row.product.photo : 'https://via.placeholder.com/220x200'}" alt="#"></a>\
            </div>\
            <div class="col-lg-4 col-md-3 col-12">\
                <h5 class="product-name">\
                    <a href="${path_product}">\
                    ${row.product.name}</a>\
                </h5>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12">\
                <div class="count-input">\
                    <input class="form-control" type="number" name="quantity" step="1" min="1" value="${formatter0.format(row.quantity)}" onchange="after_change_quantity(this);">\
                </div>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12">\
                <p class="shop-amount">${formatter.format(row.amount)}</p>\
            </div>\
            <div class="col-lg-2 col-md-2 col-12" ${cart_info.discount > 0 ? '' : 'hidden'}>\
                <p class="shop-discount">${formatter.format(row.discount)}</p>\
            </div>\
            <div class="col-lg-1 col-md-2 col-12">
                <button class="btn" onclick="delete_cart_product(this);"><i class="remove-item lni lni-close"></i></button>
            </div>
        </div>`;
        product_list.append(row_cart_order);
    }

    let total_amount_cart = document.querySelector('#shop-total-amount-cart');
    let total_amount = document.createElement('div');
    total_amount.className = 'shop-for-del';
    total_amount.innerHTML = `<ul>\
        <li>Сумма товаров в корзине<span>${formatter.format(cart_info.amount)}</span></li>\
        <li>Доставка<span>Бесплатно</span></li>\
        <li ${cart_info.discount > 0 ? '' : 'hidden'}>Скидка<span>${formatter.format(cart_info.discount)}</span></li>\
        <li class="last">К оплате<span>${formatter.format(cart_info.amount)}</span></li>\
    </ul>`;

    total_amount_cart.append(total_amount);

    // скроем кнопки если корзина пуста
    if (cart_info.quantity == 0) {
        let elements = document.querySelectorAll('.shop-for-hidden');

        for (let element of elements) {
            element.setAttribute('hidden', '');
        }
    }
}


// Получим общее количество избранных товаров
async function get_wishlist_info() {
    let wishlist_info = {
        'count': 0,
        'products': []
    };

    let options = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin'
    }

    let response = await fetch('/api/v1/get_favorite_products_info', options);

    if (!response.ok && response.status != 401) {
        console.log('Ошибка HTTP get_wishlist_info: ' + response.status);
        return wishlist_info;
    }

    wishlist_info = await response.json();

    return wishlist_info;
}

async function update_wishlist_header() {
    let wishlist_header = document.querySelector('#shop-total-wishlist');

    if (!wishlist_header) {
        return;
    }

    let wishlist_info = await get_wishlist_info();
    wishlist_header.textContent = formatter0.format(wishlist_info.count);
}


async function add_favorite_product(btn) {
    const product_pk = btn.getAttribute('data-shop-product-pk');

    let data_favorite_product = {
        product: product_pk
    };

    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(data_favorite_product)
    };

    let response = await fetch('/api/v1/add_favorite_product', options);

    if (!response.ok) {
        console.log('Ошибка HTTP add_favorite_product: ' + response.status);
        return;
    }

    update_wishlist_header();
}


async function delete_favorite_product(btn) {
    const favorite_product_pk = btn.getAttribute('data-shop-favorite_product-pk');

    let options = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin'
    };

    let response = await fetch(`/api/v1/products/favorites_delete/${favorite_product_pk}`, options);

    if (!response.ok) {
        console.log('Ошибка HTTP delete_favorite_product: ' + response.status);
        return;
    }

    // теперь удалим строку твоара на странице
    let row_favorite_product = document.querySelector(`div[data-shop-favorite_product-pk="${favorite_product_pk}"]`);

    if (row_favorite_product) {
        row_favorite_product.remove();
    }

    update_wishlist_header();
}

async function cancel_order(btn) {
    const order_pk = btn.getAttribute('data-shop-order-pk');

    let data_order = {
        'order_pk': order_pk
    };

    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(data_order)
    };

    let response = await fetch('/api/v1/cancel_order', options);

    if (!response.ok) {
        console.log('Ошибка HTTP cancel_order: ' + response.status);
        return;
    }
}

// интерактивный фильтр товаров
// async function filter_products() {

//     let params_get = '';



//     let options = {
//         method: 'GET',
//         headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
//         credentials: 'same-origin'
//     }

//     let response = await fetch('/product-list/' + params_get, options);


// }


// интерактивная сортировка товаров
async function sort_products() {
    let input_price_max = document.querySelector('input.form-range');

    if (!input_price_max) {
        console.log('Не найдена максимальная цена!');
        return;
    }

    let params_get = '?' + input_price_max.name + '=' + input_price_max.value;
    let inputs = document.querySelectorAll('input.form-check-input[checked]');

    for (let input of inputs) {
        params_get += '&' + input.name + '=' + input.value;
    }

    let select = document.getElementById('selectSorting');
    save_selectSorting(select);

    params_get += '&sorting' + '=' + select.value;

    location.href = params_get;
}

function save_selectSorting(elem) {
    sessionStorage.setItem(elem.name, elem.value);
}

function get_selectSorting(elem) {
    return sessionStorage.getItem(elem.name);
}

