

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
                <input type="number" value="${g.ranking}" name="ranking:{{g.id}}" id="ranking:${count}" style="width: 40px;" min="0" class="withoutArrows">
                <div class="verticalDiv">
                    <button type="button" class="arrowBtn" onclick="increaseRating(${count})">^</button>
                    <button type="button" class="arrowBtn" onclick="decreaseRating(${count})">v</button>
                </div>
                <input type="hidden" value="${g.id}" id="id:${g.id}" name="id:${g.id}">
                <input type="text" value="${g.genre}" name="genre:{{g.id}}" id="genre:${count}" readonly class="form-control" style="background-color:white;border:none; text-align:center">
                <input type="submit" value="Delete" name="delete:{{g.id}}" class="btn btn-outline-danger">
                <input type="submit" value="Update" name="update:{{g.id}}" class="btn btn-outline-success">
            </div>
        `
        genreBox.appendChild(genreDiv);
        count += 1;
    }
}

function increaseRating(n) {
    if (n == 1) {
        return;
    }

    let genres = window.genres.sort(compareRankings);
    console.log(genres);
    console.log(n);
    genres[n - 2].ranking += 1;
    genres[n - 1].ranking -= 1;
    setUpForm();
    // MAKE SURE TO UPDATE IDs AS WELL (then: allow the user to add new genres, then save on the backend using a for loop (make sure to update the "count" hidden form input))
}

function decreaseRating(n) {
    let genres = window.genres.sort(compareRankings);
    if (n == genres.length) {
        return;
    }

    console.log(genres);
    console.log(n);
    genres[n - 1].ranking += 1;
    genres[n].ranking -= 1;
    setUpForm();
    // MAKE SURE TO UPDATE IDs AS WELL (then: allow the user to add new genres, then save on the backend using a for loop (make sure to update the "count" hidden form input))
}