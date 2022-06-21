$(function() { 

    const validateEmail = (email) => {
        return email.match(
          /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
      };
    
    $('#form').submit(function() {
    Name = document.getElementsByName("name")[0].value
    surname = document.getElementsByName("email")[0].value
    username = document.getElementsByName("household")[0].value
    pass = document.getElementsByName("user_password")[0].value
    if (Name == null || Name == "") {
        $("#errors").html("").append("<h2 style=\"color:red\">Name field is empty</h2>")
        return false;
    }
    if (surname == null || surname == "") {
        $("#errors").html("").append("<h2 style=\"color:red\">Email field is empty</h2>")
        return false
    }
    if (!validateEmail(surname)) {
        $("#errors").html("").append("<h2 style=\"color:red\">Email is not in the right format</h2>")
        return false
    }

    if (username == null || username == "") {
        $("#errors").html("").append("<h2 style=\"color:red\">Household field is empty</h2>")
        return false
    }
    if (pass == null) {
        $("#errors").html("").append("<h2 style=\"color:red\">Password field is empty</h2>")
        return false
    }
    return true
})})