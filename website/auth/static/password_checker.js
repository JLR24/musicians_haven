
function CheckPassword() {
    // Get password inputs from the form
    const pw1 = document.getElementById("pw1");
    const pw2 = document.getElementById("pw2");

    // Check password meets requirements
    if (CheckEqual(pw1.value, pw2.value) && CheckLength(pw1.value) && CheckNumbers(pw1.value) && CheckLowerCase(pw1.value) && CheckUpperCase(pw1.value)) {
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


function CheckEqual(pw1, pw2) {
    // Checks if inputs are equal
    if (pw1 === pw2) {
        return true;
    }
    alert("Passwords must match.");
    return false;
}


function CheckLength(pw) {
    // Checks input is at least 8 characters long
    if (pw.length < 8){
        alert("Password must be at least 8 characters.");
        return false;
    }
    return true;
}


function CheckNumbers(pw) {
    // Checks the input contains at least one number
    if (pw.search(/\d/) == -1 ){
        alert("Password must contain at least one number.");
        return false;
    }
    return true;
}


function CheckLowerCase(pw) {
    // Checks the input contains at least one lowercase letter
    if (pw.search(/[a-z]/) == -1 ){
        alert("Password must contain at least lowercase letter.");
        return false;
    }
    return true;
}


function CheckUpperCase(pw) {
    // Checks the input contains at least one uppercase letter
    if (pw.search(/[A-Z]/) == -1 ){
        alert("Password must contain at least uppercase letter.");
        return false;
    }
    return true;
}