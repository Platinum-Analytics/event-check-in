// Set icon vars
let filterIcon = "bi-filter";
let alphaDown = "bi-sort-alpha-down";
let alphaUp = "bi-sort-alpha-up";
let numDown = "bi-sort-numeric-down";
let numUp = "bi-sort-numeric-up";


// Set default query params
let page = "1";
let filter = "last_name";
let desc = false;


// Set query params from url
let urlParams = new URLSearchParams(document.location.search);
if (urlParams.has("page")) {
    page = urlParams.get("page");
}
if (urlParams.has("filter")) {
    filter = urlParams.get("filter");
}
if (urlParams.has("desc")) {
    desc = urlParams.get("desc") === "True";
}


// Highlight current page number
let pageBtn = $(`#page-${page}`);
if (!pageBtn) {
    pageBtn = $("#page-1");
}
pageBtn.addClass("active");


// Highlight current filter
let filterBtn = $(`#${filter}`);
if (!filterBtn) {
    filterBtn = $("#last_name");
}
filterBtn.removeClass("btn-outline-dark").addClass("btn-dark");


// Change selected icon
let icon = filterBtn.children().first();
icon.removeClass(filterIcon);

let isAlpha = filter === "first_name" || filter === "last_name";

if (desc) {
    if (isAlpha) {
        icon.addClass(alphaUp);
    } else {
        icon.addClass(numUp);
    }
} else {
    if (isAlpha) {
        icon.addClass(alphaDown);
    } else {
        icon.addClass(numDown);
    }
}
