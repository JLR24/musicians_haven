

function Clear(type) {
    if (confirm("Are you sure you want to clear your selection?")) {
        document.getElementById(type + "_search").value = "";
        document.getElementById("added_" + type).innerHTML = "Added instrument:";
        Get(type);
        document.getElementById(type + "_missing").setAttribute("style", "display: none");
        document.getElementById(type + "_search").focus();
    }
}


function Filter(values) {
    values = values.replaceAll("&#39;", "");
    values = values.replaceAll("&amp;", "&");
    values = values.replaceAll("&#34;", "");
    values = values.replace("[", "");
    values = values.replace("]", "");
    values = values.split(", ");
    values = [...new Set(values)];
    return values;
}


function CheckMatch(value, target) { // -> bool
    var matches = 0;
    for (let val of value.split(" ")) {
        for (let tar of target.split(" ")) {
            if (tar.toLowerCase() === val.slice(0, tar.length).toLowerCase() && tar.trim() != "") {
                matches += 1;
            }
        }
    }
    if (matches == target.trim().split(" ").length) {
        return true; 
    }
    return false;
}


function AddResult(result, resultDiv, type) {
    let button = document.createElement("button");
    button.innerText = result;
    button.setAttribute("class", "btn btn-outline-secondary");
    button.setAttribute("onclick", "Add(this.innerText, '" + type + "')");
    button.setAttribute("type", "button");
    button.setAttribute("style", "margin: 3px;");
    resultDiv.appendChild(button);
}


function Get(type) {
    values = window.dict[type];
    let search = document.getElementById(type + "_search").value;
    let resultDiv = document.getElementById("searchResults_" + type); 
    let toAdd = document.getElementById(type + "s").value;
    resultDiv.innerHTML = "";

    toAdd = toAdd.split(", ");
    // // Remove from list after adding:
    // values = values.filter( function(x) {
    //     return toAdd.indexOf(x) < 0;
    // });
    document.getElementById(type + "_missing").setAttribute("style", "display: none");
    if (search.length != 0) {
        document.getElementById(type + "_missing").setAttribute("style", "display: block");
        for (let i of values) {
            if (CheckMatch(i, search)) {
                AddResult(i, resultDiv, type);
            }
        }
    }
}


function Add(value, type) {
    let resultInput = document.getElementById(type + "s");
    let added = document.getElementById("added_" + type);
    let search = document.getElementById(type + "_search");

    resultInput.value = value;

    resultInput.setAttribute("class", "true");
    added.innerText = "Added instrument: " + value;
    search.value = "";

    document.getElementById("searchResults_" + type).innerHTML = "";
    search.focus();
}


function checkEntered(type, alert=false) {
    let values = window.dict[type];
    let input = document.getElementById(type + "s").value;
    if (!values.includes(input)) {
        alert("Please enter a valid " + type + " first!");
        return false;
    }
    return true;
}