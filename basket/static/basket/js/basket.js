document.addEventListener("DOMContentLoaded", function () {

    const basketItems = document.getElementById("basketItems");
    const basketSubTotal = document.getElementById("basketSubTotal");
    const basketDeliveryFee = document.getElementById("basketDeliveryFee");
    const basketTotal = document.getElementById("basketTotal");

    if (!basketItems) {
        return;
    }

    /* retrieve date from localstroage */
    function getBasket () {
        return JSON.parse(localStorage.getItem ("umamiBasket")) || [];
    }

    function saveBasket(basket){
        localStorage.setItem("umamiBasket", JSON.stringify(basket));
    }

    /* render basket  */
    function renderBasketItems () {
        const basket = getBasket()

        /* Empty basket message */
        basketItems.innerHTML = "";
        
        if (basket.length===0){
            basketItems.innerHTML = `
            <div class="emptyBasketMessage text-center fs-2">
                <p> Your basket is empty </p>
            </div>
            `;

            if(basketSubTotal){
                basketSubTotal.textContent="0.00";
            }

        return;
        }
        
        let total =0;

        /* show basket */
        basket.forEach(function (item){
            const itemTotal = Number(item.price) * Number(item.quantity);
            total+=itemTotal;

            const orderDetail = document.createElement("div");
            orderDetail.classList.add("basket-product-card", "d-flex", "mb-3");
            
            orderDetail.innerHTML=
                `   
                    <div class="basket-product-image-wrapper">
                        ${item.image
                            ? `<img src="${item.image}" class="basket-product-image" alt="${item.name}" loading="lazy"
                                width="300" height="300">`
                            : `<div class="basket-image-placeholder">image</div>`
                        }
                    </div>


                    <div class="basket-product-content d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start">
                            <a href="${item.url || '#'}" class="text-decoration-none">
                                <h2 class="fs-6 mb-2">
                                    ${ item.name }
                                </h2>
                            </a>
                        
                            <button class="btn basket-remove-btn remove-basket-item"
                            data-product-id="${item.id}"
                            type="button"
                            aria-label="Remove ${item.name} from basket">
                                <i class="bi bi-x-lg" aria-hidden="true"></i>
                            </button>
                        </div>
                        
                            <p class="basket-product-meta mt-2 mb-2">
                                ${item.category || ""}
                                ${item.cookingTime ? ` | ${item.cookingTime}min` : ""}
                                ${item.spiceLevel ? ` | ${item.spiceLevel}` : ""}
                            </p>
                    
                        <div class="container mt-2 mb-0"> 
                            <div class="row">
                                <div class="basket-quantity-control d-inline-flex align-items-center col-6">
                                    <button class="btn basket-quantity-btn
                                            remove-basket-item"
                                            data-product-id="${item.id}"
                                            type="button"
                                            aria-label="Decrease quantity for ${item.name}">
                                            -
                                            </button>
                                    <span class="basket-quantity-number">${item.quantity}</span>
                                    <button class="btn basket-quantity-btn add-basket-item"
                                            data-product-id="${item.id}"
                                            type="button"
                                            aria-label="Increase quantity for ${item.name}">
                                            +
                                            </button>
                                </div>
                                <div class="col-6 mt-1 text-end">
                                    <p class="fs-6">
                                        £${itemTotal.toFixed(2)}
                                    </p>
                                </div>
                            </div>
                        </div>
                </div>`;
                basketItems.appendChild(orderDetail);
        });

        if (basketSubTotal){
            basketSubTotal.textContent = total.toFixed(2)
        }

        if (basketTotal){
            basketDeliveryFee.textContent = "3.99";
            const totalWithDelivery = total + parseFloat(basketDeliveryFee.textContent);
            basketTotal.textContent = totalWithDelivery.toFixed(2);
        }
    }

    basketItems.addEventListener("click", function (event)  {
        const removeButton = event.target.closest(".remove-basket-item");
        const addButton = event.target.closest(".add-basket-item");
            
            if (!removeButton && !addButton) {
                return;
            }

            event.preventDefault();
            
            const clickedButton = removeButton || addButton;
            const productId = clickedButton.dataset.productId;
            const basket = getBasket();
            
            const updatedBasket = basket
                /* remove the product if quantity by 1 */
                 .map(function (item) {
                if (item.id === productId) {
                    if (removeButton) {
                        return {
                            ...item,
                            quantity: Number(item.quantity) - 1
                        };
                    }
                    if (addButton) {
                        return {
                            ...item,
                            quantity: Math.min(Number(item.quantity) + 1, 5)
                        };
                    }
                }

                return item;
            })
                /* remove the product if quantity becomes 0 */
            .filter(function (item) {
                return Number(item.quantity) > 0;
            });
            saveBasket(updatedBasket);
            renderBasketItems();
        });
    
    renderBasketItems();

})