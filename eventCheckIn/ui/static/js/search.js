// redirect all keyboard input to search box
let searchBox = $("#search");
$(document).keypress(function () {
        if (!$(":focus").is(searchBox)) {
            searchBox.val("").focus();
        }
    }
)

// Prevent the opening of the modal when pressing the inline check in button
$(".log").each(
    function () {
        let btn = $(this)
        btn.hover(
            function () {
                btn.parent().parent().attr("data-bs-toggle", "");
            }, function () {
                btn.parent().parent().attr("data-bs-toggle", "modal");
            }
        )
    }
)

// Open the modal if there is only one search result
if ($("#searchResults").text().trim() === "1 Result") {
    new bootstrap.Modal($(".modal").first()).show();
}


