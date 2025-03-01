document.getElementById("num flashcards").addEventListener("input", function (event) {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
});