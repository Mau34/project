const password = document.getElementById("password")
const confirm_password = document.getElementById("confirm_password")
const button = document.getElementById("register")

function validatePassword(){
    if (password.value < 8) {
        password.setCustomValidity("La contraseña ingresada debe de poseer una longitud mayor o igual a 8");
    }
    else if(password.value != confirm_password.value) {
        confirm_password.setCustomValidity("La contraseñas no coinciden!");
    }
    else {
        password.setCustomValidity('');
        confirm_password.setCustomValidity('');
    }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
