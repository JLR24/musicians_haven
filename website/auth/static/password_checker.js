
function checkPassword() {
    // Get password inputs from the form
    const pw1 = document.getElementById("pw1");
    const pw2 = document.getElementById("pw2");

    // Check password meets requirements
    if (checkEqual(pw1.value, pw2.value) && checkLength(pw1.value) && checkNumbers(pw1.value) && checkLowerCase(pw1.value) && checkUpperCase(pw1.value)) {
        return true;
    }
    else {
        // Update form values
        pw1.value = "";
        pw2.value = "";
        pw1.focus();
        
        // Stop form being submiited
        stopPropagation();
        preventDefault();
    }
}


function checkEqual(pw1, pw2) {
    // Checks if inputs are equal
    if (pw1 === pw2) {
        return true;
    }
    alert("Passwords must match.");
    return false;
}


function checkLength(pw) {
    // Checks input is at least 8 characters long
    if (pw.length < 8){
        alert("Password must be at least 8 characters.");
        return false;
    }
    return true;
}


function checkNumbers(pw) {
    // Checks the input contains at least one number
    if (pw.search(/\d/) == -1 ){
        alert("Password must contain at least one number.");
        return false;
    }
    return true;
}


function checkLowerCase(pw) {
    // Checks the input contains at least one lowercase letter
    if (pw.search(/[a-z]/) == -1 ){
        alert("Password must contain at least lowercase letter.");
        return false;
    }
    return true;
}


function checkUpperCase(pw) {
    // Checks the input contains at least one uppercase letter
    if (pw.search(/[A-Z]/) == -1 ){
        alert("Password must contain at least uppercase letter.");
        return false;
    }
    return true;
}