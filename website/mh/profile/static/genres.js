

function isRankingFree(rank) {
    let count = parseInt(document.getElementById("genre_count").value);
    for (let i = 1; i <= count; i++) {
        if (rank == document.getElementById("ranking:" + i).value) {
            return false;
        }
    }
    return true;
}


function setUpForm() {
    let genreBox = document.getElementById("genreBox");
    let count = 1;
    for (g of window.genres) {
        let genreDiv = document.createElement("div");
        genreDiv.innerHTML = `
            <div class="input-group" style="border:1px dashed black; margin-bottom: 10px; border-radius: 5px;">
                <input type="number" value="${g.ranking}" name="ranking:{{g.id}}" id="ranking:${count}" style="width: 40px;" min="0" class="withoutArrows">
                <div class="verticalDiv">
                    <button type="button" class="arrowBtn" onclick="increaseRating(${count})">^</button>
                    <button type="button" class="arrowBtn" onclick="decreaseRating(${count})">v</button>
                </div>
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
    console.log(parseInt(document.getElementById("ranking:" + n).value) - 1);
}

function decreaseRating(n) {
    console.log(parseInt(document.getElementById("ranking:" + n).value) + 1);
}