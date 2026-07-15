// index.html

// shop_detail.html 
document.addEventListener("DOMContentLoaded" , function() {
    console.log("shop.js loaded");
    const productAddButtons = document.querySelectorAll(".product-add-btn");
    const orderSection = document.querySelector(".order_quantity_section");
    const favBtn = document.querySelector(".product-favourite-btn");
    const toastMessage = document.getElementById("shopToastMessage");

    console.log("Order section:", orderSection);

    const maxQuantity = 5;
    let toastTimeout;

    // Basket //
    function getBasket() {
        return JSON.parse(localStorage.getItem("umamiBasket")) || [];
    }

    function saveBasket(basket) {
    localStorage.setItem("umamiBasket", JSON.stringify(basket));
    }

    function updateBasketCount(){
        const basketCount= document.getElementById("basketCount");

        if (!basketCount){
            return;
        }

        const basket = getBasket();

        const totalItem = basket.reduce(function (total, item) {
            return total + Number(item.quantity);
        }, 0);

        basketCount.textContent = totalItem;

        if(totalItem > 0){
            basketCount.classList.remove("d-none");
        } else {
            basketCount.classList.add("d-none");
        }
    }
    
    // pop up toastmessage //
    function popUpToast(message){
        console.log("Toast element:", toastMessage);
        if (!toastMessage){ 
            return;
        }

        toastMessage.textContent = message;
        toastMessage.classList.add("show");

        clearTimeout(toastTimeout);
    
        toastTimeout = setTimeout(function() {
            console.log("Removing toast show class");
            toastMessage.classList.remove("show");
        },2000);
    }

    function addProductToBasket(product, quantityToAdd) {
        const basket = getBasket();

        const existingProduct = basket.find(function (item) {
            return item.id === product.id;
        });

        if (existingProduct) {
            existingProduct.quantity = Math.min(
                Number(existingProduct.quantity) + Number(quantityToAdd),
                maxQuantity
            );
        } else {
            basket.push({
                id: product.id,
                name: product.name,
                price: Number(product.price),
                quantity: Number(quantityToAdd),
                image: product.image,
                url: product.url,
                category: product.category,
                cookingTime: product.cookingTime,
                spiceLevel: product.spiceLevel
            });
        }

        saveBasket(basket);
        updateBasketCount();

        console.log("Basket saved:", basket);
    }
    // shop listing page //
    productAddButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                const productCard = button.closest(".product-card");

                if (!productCard) {
                    return;
                }

                const product = {
                    id: productCard.dataset.productId,
                    name: productCard.dataset.productName,
                    price: productCard.dataset.productPrice,
                    image: productCard.dataset.productImage,
                    url: productCard.dataset.productUrl,
                    category: productCard.dataset.productCategory,
                    cookingTime: productCard.dataset.productCookingTime,
                    spiceLevel: productCard.dataset.productSpiceLevel
                };
                console.log("Product image path:", product.image);
                
                addProductToBasket(product, 1);
                popUpToast("Added to Basket!");
            });
        });
               
    //add to oder button on shop detail page //
    if (orderSection) {
        console.log("Order section:", orderSection);

        const minusBtn = orderSection.querySelector(".quantity-minus");
        const plusBtn = orderSection.querySelector(".quantity-plus");
        const quantityDisplay = orderSection.querySelector(".quantity-display");
        const totalPriceDisplay = orderSection.querySelector(".product-total-price");
        const addToOrderBtn = orderSection.querySelector(".add-to-order-btn");

        const product = {
            id: orderSection.dataset.productId,
            name: orderSection.dataset.productName,
            price: Number(orderSection.dataset.productPrice),
            image: orderSection.dataset.productImage,
            url: orderSection.dataset.productUrl,
            category: orderSection.dataset.productCategory,
            cookingTime: orderSection.dataset.productCookingTime,
            spiceLevel: orderSection.dataset.productSpiceLevel
        };

        let quantity = 1;
        
        // update quantity and price //
        function updateTotalPrice() {
            const total = Number(product.price) * quantity;

            quantityDisplay.textContent = quantity;
            totalPriceDisplay.textContent = total.toFixed(2);

            plusBtn.disabled = quantity >= maxQuantity;
            minusBtn.disabled = quantity <= 1;
        }

        plusBtn.addEventListener("click", function () {
            if (quantity < maxQuantity) {
                quantity++;
                updateTotalPrice();
            }
        });

        minusBtn.addEventListener("click", function () {
            if (quantity > 1) {
                quantity--;
                updateTotalPrice();
            }
        });

        addToOrderBtn.addEventListener("click", function () {
            addProductToBasket(product, quantity);
            popUpToast("Added to Basket!");

            quantity = 1;
            updateTotalPrice();
        });

        updateTotalPrice();
    }


    // add to favourit //
    const savedMealButtons = document.querySelectorAll(".saved-meal-btn");

    function getCsrfToken() {
        const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");

        if (csrfInput) {
            return csrfInput.value;
        }

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            const trimmedCookie = cookie.trim();

            if (trimmedCookie.startsWith("csrftoken=")) {
                return trimmedCookie.substring("csrftoken=".length);
            }
        }

        return "";
    }

    savedMealButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const saveUrl = button.dataset.saveUrl;
            const icon = button.querySelector("i");

            if (!saveUrl) {
                console.log("No save URL found on favourite button");
                return;
            }

            fetch(saveUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.saved) {
                    icon.classList.remove("bi-heart");
                    icon.classList.add("bi-heart-fill");
                    button.classList.add("is-favourite");
                    popUpToast("Saved to meals!");
                } else {
                    icon.classList.remove("bi-heart-fill");
                    icon.classList.add("bi-heart");
                    button.classList.remove("is-favourite");
                    popUpToast("Removed from saved meals");
                }
            })
            .catch(function (error) {
                console.log("Saved meal error:", error);
                popUpToast("Something went wrong");
            });
        });
    });
    updateBasketCount();
});

savedMealButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const saveUrl = button.dataset.saveUrl;
        const icon = button.querySelector("i");

        fetch(saveUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken(),
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then(function (response) {
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            return response.json();
        })
        .then(function (data) {
            if (!data) {
                return;
            }

            if (data.saved) {
                icon.classList.remove("bi-heart");
                icon.classList.add("bi-heart-fill");
                popUpToast("Saved to meals!");
            } else {
                icon.classList.remove("bi-heart-fill");
                icon.classList.add("bi-heart");
                popUpToast("Removed from saved meals");
            }
        })
        .catch(function (error) {
            console.log("Saved meal error:", error);
        });
    });
});