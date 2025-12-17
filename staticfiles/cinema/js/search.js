document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchMovie");
    const movieCards = document.querySelectorAll(".movie-card");

    searchInput.addEventListener("keyup", function () {
        let value = searchInput.value.toLowerCase();

        movieCards.forEach(card => {
            let title = card.getAttribute("data-title").toLowerCase();

            if (title.includes(value)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
