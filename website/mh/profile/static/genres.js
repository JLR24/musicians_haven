

function isRankingFree(rank) {
    let count = parseInt(document.getElementById("genre_count").value);
    for (let i = 1; i <= count; i++) {
        if (rank == document.getElementById("ranking:" + i).value) {
            return false;
        }
    }
    return true;
}

function compareRankings(a, b) {
    // Source: https://javascript.plainenglish.io/how-to-sort-json-object-arrays-based-on-a-key-a157461e9610
    if (a.ranking < b.ranking) {
        return -1;
    } else if (a.ranking > b.ranking) {
        return 1;
    }
    return 0;
}


function setUpForm() {
    let genreBox = document.getElementById("genreBox");
    genreBox.innerHTML = "";
    let count = 1;

    let genres = window.genres.sort(compareRankings);

    for (g of genres) {
        let genreDiv = document.createElement("div");
        genreDiv.innerHTML = `
            <div class="input-group" style="border:1px dashed black; margin-bottom: 10px; border-radius: 5px;">
                <input type="number" value="${g.ranking}" name="ranking:${g.id}" id="ranking:${count}" style="width: 40px;" min="0" class="withoutArrows" readonly>
                <div class="verticalDiv">
                    <button type="button" class="arrowBtn" onclick="increaseRating(${count})">^</button>
                    <button type="button" class="arrowBtn" onclick="decreaseRating(${count})">v</button>
                </div>
                <input type="hidden" value="${g.id}" id="id:${g.id}" name="id:${g.id}">
                <input type="text" value="${g.genre}" name="genre:${g.id}" id="genre:${count}" readonly class="form-control" style="background-color:white;border:none; text-align:center">
                <button type="button" class="btn btn-outline-warning" onclick="removeGenre('${g.genre}')">Delete</button>
            </div>
        `
        // <input type="submit" value="Update" name="update:${g.id}" class="btn btn-outline-success">
        // <input type="submit" value="Delete" name="delete:${g.id}" class="btn btn-outline-warning" onclick="removeGenre(${g.genre})">
        genreBox.appendChild(genreDiv);
        count += 1;
    }
}

function increaseRating(n) {
    if (n == 1) {
        return;
    }

    let genres = window.genres.sort(compareRankings);
    genres[n - 2].ranking += 1;
    genres[n - 1].ranking -= 1;
    setUpForm();
}

function decreaseRating(n) {
    let genres = window.genres.sort(compareRankings);
    if (n == genres.length) {
        return;
    }

    genres[n - 1].ranking += 1;
    genres[n].ranking -= 1;
    setUpForm();
}


function GetGenre() {
    values = window.dict["genre"];
    let search = document.getElementById("genre_search").value;
    let resultDiv = document.getElementById("searchResults_genre");
    resultDiv.innerHTML = "";

    document.getElementById("genre_missing").setAttribute("style", "display:none");
    if (search.length != 0) {
        let count = 0;
        document.getElementById("genre_missing").setAttribute("style", "display: block");
        for (let i of values) {
            if (CheckOrderedMatch(i, search)) {
                AddGenreResult(i, resultDiv);
                count += 1;
            }
        }
        if (count > 50) {
            resultDiv.innerHTML = "Too many values to display, please type more of the word...";
        }
    }
}


function AddGenreResult(result, resultDiv) {
    let button = document.createElement("button");
    button.innerText = result;
    button.setAttribute("class", "btn btn-outline-secondary");
    button.setAttribute("onclick", "AddGenre(this.innerText)");
    button.setAttribute("type", "button");
    button.setAttribute("style", "margin: 3px");
    resultDiv.appendChild(button);
}


function AddGenre(genre) {
    // Remove from list in window.dict;
    values = window.dict["genre"];
    for (i of values) {
        if (i === genre) {
            values.splice(values.indexOf(i), 1);
        }
    }
    
    // Add to dict of user genres.
    let genre_count = document.getElementById("genre_count");
    let count = parseInt(genre_count.value);
    window.genres.push({
        "id": (count + 1),
        "user": "N/A",
        "genre": genre,
        "ranking": (count + 1)
    });
    document.getElementById("genre_count").value = parseInt(document.getElementById("genre_count").value) + 1;

    // Reload form and clear selection:
    setUpForm();
    ClearGenre();
}


function ClearGenre() {
    document.getElementById("genre_search").value = "";
    GetGenre();
    document.getElementById("genre_missing").setAttribute("style", "display: none");
    document.getElementById("genre_search").focus();
}


function removeGenre(genre) {
    // Add back to list in window.dict:
    window.dict["genre"].push(genre);
    
    // Remove from window.genres:
    let index = 0;
    let toRemove;
    for (g of window.genres) {
        if (g.genre == genre) {
            index = window.genres.indexOf(g);
            toRemove = g;
        }
    }
    window.genres.splice(index, 1);

    // Check for anything after and move up.
    for (g of window.genres) {
        if (parseInt(g.ranking) > parseInt(toRemove.ranking)) {
            let index = window.genres.indexOf(g);
            window.genres[index].ranking = parseInt(window.genres[index].ranking) - 1;
        }
    }

    document.getElementById("genre_count").value = parseInt(document.getElementById("genre_count").value) - 1;

    // Reload form:
    setUpForm();
    ClearGenre();
}