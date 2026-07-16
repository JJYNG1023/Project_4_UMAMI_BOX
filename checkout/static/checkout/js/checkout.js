document.addEventListener("DOMContentLoaded", function () {
    console.log("checkout.js loaded");

    const checkoutBasketItems = document.getElementById("checkoutBasketItems");
    const checkoutSubTotal = document.getElementById("checkoutSubTotal");
    const checkoutDeliveryFee = document.getElementById("checkoutDeliveryFee");
    const checkoutTotal = document.getElementById("checkoutTotal");

    function getBasket() {
        return JSON.parse(localStorage.getItem("umamiBasket")) || [];
    }

    function renderCheckoutBasket() {
        const basket = getBasket();

        let subTotal = 0;

        if (checkoutBasketItems) {
            checkoutBasketItems.innerHTML = "";
        }

        if (basket.length === 0) {
            if (checkoutBasketItems) {
                checkoutBasketItems.innerHTML = `
                    <div class="emptyBasketMessage">
                        <p>Your basket is empty.</p>
                    </div>
                `;
            }

            if (checkoutSubTotal) {
                checkoutSubTotal.textContent = "0.00";
            }

            if (checkoutDeliveryFee) {
                checkoutDeliveryFee.textContent = "0.00";
            }

            if (checkoutTotal) {
                checkoutTotal.textContent = "0.00";
            }

            return;
        }

        basket.forEach(function (item) {
            const itemTotal = Number(item.price) * Number(item.quantity);
            subTotal += itemTotal;

            if (checkoutBasketItems) {
                const orderDetail = document.createElement("div");
                orderDetail.classList.add("basket-product-card", "d-flex", "mb-3");

                orderDetail.innerHTML = `
                    <div class="basket-product-image-wrapper">
                        ${item.image
                            ? `<img src="${item.image}" class="basket-product-image" alt="${item.name}">`
                            : `<div class="basket-image-placeholder">image</div>`
                        }
                    </div>

                    <div class="basket-product-content d-flex flex-column">
                        <h3 class="fs-6 mb-2">
                            ${item.name}
                        </h3>

                        <p class="basket-product-meta mt-2 mb-2">
                            ${item.category || ""}
                            ${item.cookingTime ? ` | ${item.cookingTime} min` : ""}
                            ${item.spiceLevel ? ` | ${item.spiceLevel}` : ""}
                        </p>

                        <p class="basket-product-price mb-2">
                            £${Number(item.price).toFixed(2)}
                        </p>

                        <p class="mb-1">
                            Quantity: ${item.quantity}
                        </p>

                        <p class="fw-bold mt-auto mb-0">
                            Item total: £${itemTotal.toFixed(2)}
                        </p>
                    </div>
                `;

                checkoutBasketItems.appendChild(orderDetail);
            }
        });

        const deliveryFee = subTotal > 0 ? 3.99 : 0;
        const total = subTotal + deliveryFee;

        if (checkoutSubTotal) {
            checkoutSubTotal.textContent = subTotal.toFixed(2);
        }

        if (checkoutDeliveryFee) {
            checkoutDeliveryFee.textContent = deliveryFee.toFixed(2);
        }

        if (checkoutTotal) {
            checkoutTotal.textContent = total.toFixed(2);
        }
    }

    renderCheckoutBasket();
});