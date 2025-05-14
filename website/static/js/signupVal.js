function signupVal(event) {
    var form = document.getElementById("signupform");

    var firstname = document.getElementById("firstName").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password1").value;
    var password2 = document.getElementById("password2").value;

    // Clear previous errors
    document.getElementById("emailerror").innerHTML = "";
    document.getElementById("passworderror").innerHTML = "";
    document.getElementById("firstnameerror").innerHTML = "";
    document.getElementById("password2error").innerHTML = "";

    var pass = true;

    // Email validation
    if (!email.trim()) {
        document.getElementById("emailerror").innerHTML = "Error: email is empty";
        pass = false;
    } else if (email.length > 45) {
        document.getElementById("emailerror").innerHTML = "Error: email is too long (max: 45)";
        pass = false;
    } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById("emailerror").innerHTML = "Error: Invalid email format";
        pass = false;
    }

    // Password validation
    if (!password.trim()) {
        document.getElementById("passworderror").innerHTML = "Error: Password is empty";
        pass = false;
    } else if (password.length > 15) {
        document.getElementById("passworderror").innerHTML = "Password too long (Max: 15)";
        pass = false;
    } else if(password.length < 7){
        document.getElementById("passworderror").innerHTML = "Password too long (Min: 7)";
        pass = false;
    }

    // First name validation (Fixed)
    if (!firstname.trim()) {
        document.getElementById("firstnameerror").innerHTML = "Error: First name is empty";
        pass = false;
    } else if (firstname.length > 30) {
        document.getElementById("firstnameerror").innerHTML = "Error: First name too long (Max: 30)";
        pass = false;
    } else if (firstname.length < 3) {
        document.getElementById("firstnameerror").innerHTML = "Error: First name too short (Min: 3)";
        pass = false;
    }

    // Confirm password validation
    if (password !== password2) {
        document.getElementById("password2error").innerHTML = "Passwords need to match";
        pass = false;
    }

    // Prevent form submission if validation fails
    if (!pass) {
        event.preventDefault();
        console.log("Form submission prevented due to validation errors.");
    }
}