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
