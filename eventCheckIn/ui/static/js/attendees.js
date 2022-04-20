// Expand/Collapse Student Guests
let guestBtns = document.getElementsByClassName("expand-guest");

for (let i = 0; i < guestBtns.length; i++) {
    guestBtns[i].addEventListener("click", function () {
        if (this.title === "Show Guests") {
            expandGuest(this);
        } else {
            collapseGuest(this);
        }
    })
}

let collapseAll = document.getElementById("all-guests")

collapseAll.addEventListener("click", function () {
    let isCollapsed = this.innerHTML === "Show All";
    for (let i = 0; i < guestBtns.length; i++) {
        let btn = guestBtns[i]
        let btnCollapsed = btn.title === "Show Guests"

        if (!(isCollapsed || btnCollapsed)) {
            collapseGuest(btn);
        } else if (isCollapsed && btnCollapsed) {
            expandGuest(btn);
        }
    }

    this.innerHTML = isCollapsed ? "Collapse All" : "Show All";
})

function collapseGuest(guestBtn) {
    let rows = document.querySelectorAll(`tr[parent_id='${guestBtn.getAttribute('parent_id')}']`)

    guestBtn.children[0].className = "fa-solid fa-chevron-down"
    guestBtn.title = "Show Guests"

    for (let j = 0; j < rows.length; j++) {
        rows[j].style.display = "none"
    }
}

function expandGuest(guestBtn) {
    let rows = document.querySelectorAll(`tr[parent_id='${guestBtn.getAttribute('parent_id')}']`)

    guestBtn.children[0].className = "fa-solid fa-chevron-up"
    guestBtn.title = "Hide Guests"

    for (let j = 0; j < rows.length; j++) {
        rows[j].style.display = ""
    }
}
