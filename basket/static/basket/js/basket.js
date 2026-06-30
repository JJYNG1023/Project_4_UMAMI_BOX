document.addEventListener("DOMContentLoaded", function () {
    console.log("basket.js loaded");

    const basketItems = document.getElementById("basketItems");

    if (!basketItems) {
        console.log("basketItems container not found");
        return;
    }

    /* retrieve date from localstroage */
    function getBasket () {
        return JSON.parse(localStorage.getItem ("umamiBasket")) || [];
    }

    /* render basket  */
    function renderBasketItems () {
        const basket = getBasket()

        console.log("basket:",basket);

        /* Empty basket message */
        basketItems.innerHTML = "";
        
        if (basket.length===0){
        basketItems.innerHTML = `
        <div class="emptyBasketMessage">
            <p> Your basket is empty </p>
        <div>
        `;
        return;
        }
        
        /* show basket */
        basket.forEach(function (item){
            const itemTotal = Number(item.price) * Number(item.quantity);
            const orderDetail = document.createElement("div");
            orderDetail.classList.add("orderDetail","mb-3");
            
            orderDetail.innerHTML=
                `   <div class="product-card-content d-flex flex-column">
                        <a href="#" class="text-decoration-none">
                            <h3 class="product-title mb-2">
                                ${ item.name }
                            </h3>
                        </a>

                        <div class="product-card-bottom d-flex justify-content-between align-items-center mt-auto">
                            <p class="product-price mb-0">
                                £ ${Number(item.price).toFixed(2)}
                            </p>

                            <p class="mb-1">
                                Quantity: ${item.quantity}
                            </p>

                            <p class="fw-bold mb-0">
                                Item total: £${itemTotal.toFixed(2)}
                            </p>
                        </div>
                    </div>`;
                basketItems.appendChild(orderDetail);
        });
    }

    renderBasketItems();
})