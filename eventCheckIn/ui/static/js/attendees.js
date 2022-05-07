// Set icon vars
let filterIcon = "bi-filter";
let alphaDown = "bi-sort-alpha-down";
let alphaUp = "bi-sort-alpha-up";
let numDown = "bi-sort-numeric-down";
let numUp = "bi-sort-numeric-up";


// Set default query params
let page = "1";
let filter = "ticket_num";
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
let pageBtn = document.getElementById(`page-${page}`);
if (!pageBtn) {
    pageBtn = document.getElementById("page-1");
}
pageBtn.classList.add("active");


// Highlight current filter
let filterBtn = document.getElementById(filter);
if (!filterBtn) {
    filterBtn = document.getElementById("ticket_num");
}
filterBtn.classList.remove("btn-outline-dark");
filterBtn.classList.add("btn-dark");


// Change selected icon
let icon = filterBtn.firstElementChild;
icon.classList.remove(filterIcon);

let isAlpha = filter === "first_name" || filter === "last_name";

if (desc) {
    if (isAlpha) {
        icon.classList.add(alphaUp);
    } else {
        icon.classList.add(numUp);
    }
} else {
    if (isAlpha) {
        icon.classList.add(alphaDown);
    } else {
        icon.classList.add(numDown);
    }
}
