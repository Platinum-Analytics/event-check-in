// Recreate file upload label
let csvUpload = document.getElementById("csv")

csvUpload.addEventListener("change", function () {
    document.getElementById("csvLbl").innerHTML = csvUpload.value.split("\\").pop();
})
