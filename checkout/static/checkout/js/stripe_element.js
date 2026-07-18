document.addEventListener("DOMContentLoaded", function () {
    console.log("checkout.js loaded");

    const paymentForm = document.getElementById("payment-form");
    const cardErrors = document.getElementById("card-errors");

    const stripePublicKeyElement = document.getElementById("id_stripe_public_key");
    const clientSecretElement = document.getElementById("id_client_secret");

    if (!paymentForm || !stripePublicKeyElement || !clientSecretElement) {
        console.log("Stripe form elements not found");
        return;
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

    const card = elements.create("card", {
        style: style
    });

    card.mount("#card-element");

    card.addEventListener("change", function (event) {
        if (event.error) {
            cardErrors.textContent = event.error.message;
        } else {
            cardErrors.textContent = "";
        }
    });

    paymentForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const submitButton = paymentForm.querySelector("button[type='submit']");
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: paymentForm.full_name.value.trim(),
                    email: paymentForm.email.value.trim(),
                    phone: paymentForm.phone_number.value.trim(),
                    address: {
                        line1: paymentForm.street_address_1.value.trim(),
                        line2: paymentForm.street_address_2.value.trim(),
                        postal_code: paymentForm.postcode.value.trim(),
                        city: paymentForm.town_or_city.value.trim(),
                        country: paymentForm.country.value
                    }
                }
            }
        }).then(function (result) {
            if (result.error) {
                cardErrors.textContent = result.error.message;
                submitButton.disabled = false;
                submitButton.textContent = "Continue to Payment";
            } else {
                if (result.paymentIntent.status === "succeeded") {
                    paymentForm.submit();
                }
            }
        });
    });
});