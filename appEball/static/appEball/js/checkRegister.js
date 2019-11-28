if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main() {
    var usernameInput = document.getElementById('id_username');
    var emailInput = document.getElementById('id_email');
    var ccNumberInput = document.getElementById('id_ccNumber');
    var phoneNumberInput = document.getElementById('id_phoneNumber');
    usernameInput.addEventListener('change', function(e) {
        ajaxRegister(e, 'username', usernameInput);
    });
    emailInput.addEventListener('change', function(e) {
        ajaxRegister(e, 'email', emailInput);
    });
    ccNumberInput.addEventListener('change', function(e) {
        ajaxRegister(e, 'ccNumber', ccNumberInput);
    });
    phoneNumberInput.addEventListener('change', function(e) {
        ajaxRegister(e, 'phoneNumber', phoneNumberInput);
    });
}

function ajaxRegister(e, dataType, input) {
    var value = input.value;

    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token
        }
    });

    $.ajax({
        url: 'checkRegister/',
        data: JSON.stringify({type: dataType, value: value}),
        type: 'PATCH',
        contentType: 'application/json',
        success: (response) => {
            if (response.is_taken=='username') {
                $('#id_username').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>A user with this username already exists! Try another one.</div>"
                );
            } else if (response.is_taken=='email') {
                $('#id_email').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>A user with this email already exists! Try another one.</div>"
                );
            } else if (response.is_taken=='ccNumber') {
                $('#id_ccNumber').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>A user with this CC number already exists!</div>"
                );
            } else if (response.is_taken=='phoneNumber') {
                $('#id_phoneNumber').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>A user with this phone number already exists!</div>"
                );
            }
        },
        failure: (response) => {
            console.log('FAILURE -> ', response);
        }
    })
}