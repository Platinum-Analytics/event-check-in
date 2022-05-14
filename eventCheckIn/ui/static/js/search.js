// redirect all keyboard input to search box
let searchBox = $("#search");
$(document).keypress(function () {
        if (!$(":focus").is(searchBox)) {
            searchBox.val("").focus();
        }
    }
)

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

if ($("#searchResults").text().trim() === "1 Result") {
    new bootstrap.Modal($(".modal").first()).show();
}


