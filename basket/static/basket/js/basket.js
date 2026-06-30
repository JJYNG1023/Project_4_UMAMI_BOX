document.addEventListener("DOMContentLoaded", function () {
    console.log("basket.js loaded");

    const basketItems = document.getElementById("basketItems");
    const basketTotal = document.getElementById("basketTotal");

    if (!basketItems) {
        console.log("basketItems container not found");
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

        console.log("basket:",basket);

        /* Empty basket message */
        basketItems.innerHTML = "";
        
        if (basket.length===0){
            basketItems.innerHTML = `
            <div class="emptyBasketMessage">
                <p> Your basket is empty </p>
            <div>
            `;

            if(basketTotal){
                basketTotal.textContent="0.00";
            }

        return;
        }
        
        let total =0;

        /* show basket */
        basket.forEach(function (item){
            const itemTotal = Number(item.price) * Number(item.quantity);
            total+=itemTotal;

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
                        <button class="btn remove-basket-item mt-2" data-product-id="${item.id}" type="button">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>`;
                basketItems.appendChild(orderDetail);
        });

        if (basketTotal){
            basketTotal.textContent = total.toFixed(2)
        }
    }

    basketItems.addEventListener("click", function (event)  {
        const removeButton = event.target.closest(".remove-basket-item");            
            if (!removeButton) {
                return;
            }
            console.count("remove clicked")

            event.preventDefault();
            
            const productId = removeButton.dataset.productId;
            const basket = getBasket();
            
            const updatedBasket = basket
                /* remove the product if quantity by 1 */
                .map(function (item){
                    if (item.id === productId){
                        return { 
                            ...item,
                            quantity: item.quantity - 1
                        };
                    }
                    return item;
                })
                /* remove the product if quantity becomes 0 */
                .filter(function (item) {
                    return item.quantity>0;
                });
            saveBasket(updatedBasket);
            renderBasketItems();
        });
    
    renderBasketItems();

})