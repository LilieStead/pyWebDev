function loginVal(event){ 
    var form = document.getElementById("loginform");

    var email = form.email.value;
    var password = form.password.value;

    // Clear previous errors
    document.getElementById("emailerror").innerHTML = "";
    document.getElementById("passworderror").innerHTML = "";

    var pass = true;

    if (email == null || email.trim() === "") {
        document.getElementById("emailerror").innerHTML = "Error: email is empty";
        pass = false;
    } else if (email.length > 45) {
        document.getElementById("emailerror").innerHTML = "Error: email is too long (max: 45)";
        pass = false;
    } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById("emailerror").innerHTML = "Error: Invalid email format";
        pass = false;
}


    if (password == null || password.trim() === "") {
        document.getElementById("passworderror").innerHTML = "Error: Password is empty";
        pass = false;
    } else if (password.length > 15) {
        document.getElementById("passworderror").innerHTML = "Password too long (Max: 15)";
        pass = false;
    }

    // Prevent form submission if validation fails
    if (!pass) {
        event.preventDefault();
        console.log("Form submission prevented due to validation errors.");
    }
}