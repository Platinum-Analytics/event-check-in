// Set default query params
let page = 1
let filter = "ticket_num"

// Set query params from url
let urlParams = new URLSearchParams(document.location.search)
if (urlParams.has("page")) { page = urlParams.get("page") }
if (urlParams.has("filter")) { filter = urlParams.get("filter") }

// Highlight current page number
document.getElementById(`page-${page}`).classList.add("active");

// Highlight current filter
let filterBtn = document.getElementById(filter);
filterBtn.classList.remove("btn-outline-dark");
filterBtn.classList.add("btn-dark");
