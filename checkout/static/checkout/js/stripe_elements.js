document.addEventListener("DOMContentLoaded", function () {
    console.log("checkout.js loaded");
    console.log("stripe_elements.js loaded");

    const paymentForm = document.getElementById("payment-form");
    const cardErrors = document.getElementById("card-errors");
    const paymentIntentIdInput = document.getElementById("paymentIntentId");
    const billingPostcodeInput = document.getElementById("billingPostcode");

    const stripePublicKeyElement = document.getElementById("id_stripe_public_key");
    const clientSecretElement = document.getElementById("id_client_secret");

    if (!paymentForm || !stripePublicKeyElement || !clientSecretElement) {
        console.log("Stripe form elements not found");
        return;
    }
    
    function getJsonScriptValue(id) {
        const element = document.getElementById(id);

        if (!element) {
            return "";
        }

        return JSON.parse(element.textContent);
    }

    const stripePublicKey = JSON.parse(stripePublicKeyElement.textContent);
    const clientSecret = JSON.parse(clientSecretElement.textContent);

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    const style = {
        base: {
            color: "#123525",
            fontFamily: "Inter, Arial, sans-serif",
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
                color: "#8a8a8a"
            }
        },
        invalid: {
            color: "#dc3545",
            iconColor: "#dc3545"
        }
    };

    const cardNumber = elements.create("cardNumber", {
        style: style
    });

    const cardExpiry = elements.create("cardExpiry", {
        style: style
    });

    const cardCvc = elements.create("cardCvc", {
        style: style
    });
    
    cardNumber.mount("#card-number-element");
    cardExpiry.mount("#card-expiry-element");
    cardCvc.mount("#card-cvc-element");

    function showCardError(event) {
        if (event.error) {
            cardErrors.textContent = event.error.message;
        } else {
            cardErrors.textContent = "";
        }
    }

    cardNumber.addEventListener("change", showCardError);
    cardExpiry.addEventListener("change", showCardError);
    cardCvc.addEventListener("change", showCardError);

    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const submitButton = paymentForm.querySelector("button[type='submit']");
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        const postcode = billingPostcodeInput
            ? billingPostcodeInput.value.trim()
            : getJsonScriptValue("order_postcode");

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardNumber,
                billing_details: {
                    name: getJsonScriptValue("order_full_name"),
                    email: getJsonScriptValue("order_email"),
                    phone: getJsonScriptValue("order_phone_number"),
                    address: {
                        line1: getJsonScriptValue("order_street_address_1"),
                        line2: getJsonScriptValue("order_street_address_2"),
                        postal_code: postcode,
                        city: getJsonScriptValue("order_town_or_city"),
                        country: getJsonScriptValue("order_country")
                    }
                }
            }
        }).then(function (result) {
            console.log('stripe result:', result);
            
            if (result.error) {
                cardErrors.textContent = result.error.message;
                submitButton.disabled = false;
                submitButton.textContent = "Complete Payment";
                return;
                }

                if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
                    paymentIntentIdInput.value = result.paymentIntent.id;
                    paymentForm.submit();
                    return;
                }
                cardErrors.textContent = "Payment was not completed. Please try again";
                submitButton.disabled = false;
                submitButton.textContent = "Complete payment";
            });
        });
    });