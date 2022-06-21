$(function() { 

    const validateEmail = (email) => {
        return email.match(
          /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
      };
    
    $('#form').submit(function() {
    surname = document.getElementsByName("email")[0].value
    username = document.getElementsByName("household")[0].value
    
    if (surname == null || surname == "") {
        $("#errors").append($("h2").append("Email field is empty"))
        return false
    }
    if (!validateEmail(surname)) {
        $("#errors").append($("h2").append("Email is not in the right format"))
        return false
    }

    if (username == null || username == "") {
        $("#errors").append($("h2").append("Household field is empty"))
        return false
    }
    pass = document.getElementsByName("user_password")[0].value
    passConf = document.getElementById("PasswordConfirmation").value
    if (pass != passConf) {
        $("#errors").append($("h2").append("Password field is empty"))
        return false
    }
    return false
})})