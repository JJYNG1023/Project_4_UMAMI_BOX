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
    if (favBtn) {
        favBtn.addEventListener("click", function () {
            const icon = favBtn.querySelector("i");

            favBtn.classList.toggle("is-favourite");

            if (icon) {
                icon.classList.toggle("bi-heart");
                icon.classList.toggle("bi-heart-fill");
            }

            popUpToast(`Added To Favourite`);
        });
    }
    updateBasketCount();
});

