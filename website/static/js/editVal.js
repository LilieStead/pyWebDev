function editVal(event) {
    var form = document.getElementById("profileform");

    var firstName = form.firstName.value.trim();
    var email = form.email.value.trim();
    var password1 = form.password1.value;
    var password2 = form.password2.value;

    // Clear previous errors
    document.getElementById("firstNameerror").textContent = "";
    document.getElementById("emailerror").textContent = "";
    document.getElementById("password1error").textContent = "";
    document.getElementById("password2error").textContent = "";

    var pass = true;

    if (firstName.length === 0) {
        document.getElementById("firstNameerror").textContent = "First name cannot be empty.";
        pass = false;
    } else if (firstName.length < 2) {
        document.getElementById("firstNameerror").textContent = "First name is too short (Min 2 characters)";
        pass = false;
    } else if (firstName.length > 30) {
        document.getElementById("firstNameerror").textContent = "First name is too long (Max 30 characters)";
        pass = false;
    }

    // Email validation (required)
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
        document.getElementById("emailerror").textContent = "Email cannot be empty.";
        pass = false;
    } else if (email.length > 45) {
        document.getElementById("emailerror").textContent = "Email is too long (max 45 characters).";
        pass = false;
    } else if (!emailRegex.test(email)) {
        document.getElementById("emailerror").textContent = "Invalid email format.";
        pass = false;
    }

    // Password validation only if new password is entered
    if (password1.length > 0) {
        if (password1.length < 7) {
            document.getElementById("password1error").textContent = "Password must be at least 7 characters.";
            pass = false;
        } else if (password1.length > 15) {
            document.getElementById("password1error").textContent = "Password is too long (max 15 characters).";
            pass = false;
        }

        if (password1 !== password2) {
            document.getElementById("password2error").textContent = "Passwords do not match.";
            pass = false;
        }
    }

    if (!pass) {
        event.preventDefault(); // prevent form submit
        console.log("Form submission prevented due to validation errors.");
    }
}