// index.html

// shop_detail.html 
document.addEventListener("DOMContentLoaded" , function() {
    console.log("shop.js loaded");
    
    const orderSection = document.querySelector(".order_quantity_section");
    console.log("Order section:", orderSection);


    if (!orderSection){
        console.log("No order section found");
        return;
    }

    const minusBtn = document.querySelector(".quantity-minus");
    const plusBtn = document.querySelector(".quantity-plus");
    const quantityDisplay = document.querySelector(".quantity-display");
    const totalPriceDisplay = document.querySelector(".product-total-price");
    const addToOrderBtn = document.querySelector(".add-to-order-btn");
    const favBtn = document.querySelector(".product-favourite-btn");
    const toastMessage = document.getElementById("shopToastMessage");

    const productId = orderSection.dataset.productId
    const productName = orderSection.dataset.productName;
    const productPrice = parseFloat (orderSection.dataset.productPrice);
    console.log("Product detail:", productId, productName, productPrice);

    let quantity = 1 ;
    const maxQuantity = 5;
    let toastTimeout;

    // update quantity and price //
    function updateTotalPrice () {
        const total = productPrice * quantity;
        quantityDisplay.textContent = quantity;
        totalPriceDisplay.textContent = total.toFixed(2);
    }

        plusBtn.addEventListener("click",function (){
            if (quantity < 5) {
                quantity ++;
                updateTotalPrice();
            };
        });

        minusBtn.addEventListener("click",function (){
            if (quantity > 1){
                quantity --;
                updateTotalPrice()
            }
        });

    updateTotalPrice();

    //add order button//


    // add order Basket //
    addToOrderBtn.addEventListener("click", function(){
        const basket = getBasket();
        const existingProduct = basket.find(function(item){
            return item.id === productId;
        });

        if (existingProduct){
            existingProduct.quantity = Math.min(existingProduct.quantity + quantity, maxQuantity);
        }else{
            basket.push({
                id: productId,
                name: productName,
                price: productPrice,
                quantity:quantity
            });  
        }

        saveBasket(basket);
        updateBasketCount();

        popUpToast(`Added to Basket !`);
    });

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

        const totalItem = basket.reduce(function (total ,item){
            return total + item.quantity;
        },0);

        basketCount.textContent = totalItem;

        if(totalItem > 0){
            basketCount.classList.remove("d-none");
        } else {
            basketCount.classList.add("d-none");
        }
    }
    

    // pop up toastmessage //
    function popUpToast(message){
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
    updateTotalPrice();
});

