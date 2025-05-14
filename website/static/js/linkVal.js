function linkVal(event) {
    var form = document.getElementById("linkform");
    var link = form.link.value;

    // Clear previous errors
    document.getElementById("linkerror").innerHTML = "";

    var pass = true;

    // Regex to match Amazon links
    var amazonRegex = /^(https?:\/\/)?(www\.)?amazon\.(com|co\.uk|de|fr|ca|jp|in|it|es|cn|br|mx|au)\/.+$/;

    if (!link) {
        document.getElementById("linkerror").innerHTML = "Error: Link is empty";
        pass = false;
    } else if (!amazonRegex.test(link)) {
        document.getElementById("linkerror").innerHTML = "Error: Invalid Amazon link";
        pass = false;
    }

    // Prevent form submission if validation fails
    if (!pass) {
        event.preventDefault();
        console.log("Form submission prevented due to validation errors.");
    }
}