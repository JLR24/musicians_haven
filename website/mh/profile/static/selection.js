

function GetSelectedObject(type) {
    let currentSelection = document.getElementById(type + "_select").value;

    for (let x of window.user_[type]) {
        document.getElementById(type + "_" + x.id).setAttribute("style", "display: none;");
        if (x.id == currentSelection) {
            document.getElementById(type + "_add").setAttribute("style", "display: none;");
            document.getElementById(type + "_" + x.id).setAttribute("style", "display: block;");
            window[type] = x;
        }
    }

    if (currentSelection == "Add New") {
        document.getElementById(type + "_add").setAttribute("style", "display: block;");
    }
}