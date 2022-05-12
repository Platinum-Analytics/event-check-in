// redirect all keyboard input to search box
let searchBox = $("#search");
$(document).keypress(function () {
        if (!$(":focus").is(searchBox)) {
            searchBox.val("").focus();
        }
    }
)
