const card = document.getElementById("cardNumber")
const exp_date = document.getElementById("expiryDate")
const CVV = document.getElementById("cvv")
const quantity = document.getElementById("quantity")

function validateCard() {
    if (card.value.length == 8 && card.value.match(/([A-z])|(\s)/) == null) {
        card.setCustomValidity('');
    } else {
        card.setCustomValidity("El numero de tarjeta bancario no es valido!");
    }
}

function validateExp() {
    if (exp_date.value.match(/\d\d-\d\d\d\d/) != null) {
        exp_date.setCustomValidity('');
    } else {
        exp_date.setCustomValidity("La fecha de vencimiento no es valida");
    }
}

function validateCVV() {
    if (CVV.value.match(/\d\d\d/) != null) {
        CVV.setCustomValidity('');
    } else {
        CVV.setCustomValidity("El CVV no es valido");
    }
}

quantity.addEventListener("keypress", function (evt) {
    if (evt.which < 48 || evt.which > 57)
    {
        evt.preventDefault();
    }
});


card.onchange = validateCard;
exp_date.onchange = validateExp;
CVV.onchange = validateCVV;
