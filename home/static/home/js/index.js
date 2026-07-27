document.addEventListener ("DOMContentLoaded", function(){
    const contactForm = document.getElementById("contactForm");
    const formMessafe = document.getElementById("formMessage");

    if (contactForm){
        contactForm.addEventListener("submit",function (event){
            event.preventDefault()

            formMessage.textContent = "Your enquiry has been sent";
            formMessage.classList.remove("d-none");
            contectForm.rest();
        });
    }
});