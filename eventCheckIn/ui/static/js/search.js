let searchBox = document.getElementById("search");

// redirect all keyboard input to search box
document.addEventListener('keydown', function () {
    if (document.activeElement !== searchBox) {
        searchBox.value = "";
        searchBox.focus();
    }
})
