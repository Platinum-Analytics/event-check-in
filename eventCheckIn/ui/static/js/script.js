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
        console.log(this)
        let row = document.getElementById(`parent${this.id}`)
        if (row.style.display === 'none') {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    })
}


