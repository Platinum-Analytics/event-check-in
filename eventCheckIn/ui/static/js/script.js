let closeBtns = document.getElementsByClassName("closeBtn");

for (let i = 0; i < closeBtns.length; i++) {
    closeBtns[i].onclick = function () {
        let parentStyle = this.parentElement.style
        parentStyle.opacity = "0";

        setTimeout(function () {
            parentStyle.display = "none";
        }, 600);
    }
}

let guestBtns = document.getElementsByClassName("expand-guest");

for (let i = 0; i < guestBtns.length; i++) {
    guestBtns[i].addEventListener("click", function () {
        let rows = document.querySelectorAll(`tr[parent_id='${this.getAttribute('parent_id')}']`)

        if (rows[0].style.display === 'none') {
            this.children[0].className = "fa fa-chevron-up"
            this.children[0].title = "Hide Guests"

            for (let j = 0; j < rows.length; j++) {
                rows[j].style.display = ""
            }

        } else {
            this.children[0].className = "fa fa-chevron-down"
            this.children[0].title = "Show Guests"

            for (let j = 0; j < rows.length; j++) {
                rows[j].style.display = "none"
            }
        }
    })
}

let csvUpload = document.getElementById("csv")

csvUpload.addEventListener("change", function () {
    let fileName = csvUpload.value.split("\\").pop()
    let csvLbl = document.getElementById("csvLbl")
    csvLbl.innerHTML=fileName;
})


