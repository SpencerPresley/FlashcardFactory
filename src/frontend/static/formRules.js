document
  .getElementById("num_flash_cards")
  .addEventListener("input", function (event) {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
  });

const form = document.getElementById("form");

form.addEventListener("submit", function (event) {
  //event.preventDefault(); // Prevents the default form submission

  form.submit();
  console.log(response);
});

const fileInput = document.getElementById("fileInput");
const fileUploadContainer = document.getElementById("fileUploadContainer");
const fileList = document.getElementById("fileList");

// Handle file selection (either via button or drag-and-drop)
fileInput.addEventListener("change", handleFiles);

// Handle drag-over event (needed to allow dropping files)
fileUploadContainer.addEventListener("dragover", function (event) {
  event.preventDefault();
  fileUploadContainer.classList.add("dragover");
});

// Handle drag-leave event
fileUploadContainer.addEventListener("dragleave", function (event) {
  fileUploadContainer.classList.remove("dragover");
});

// Handle drop event (files being dropped)
fileUploadContainer.addEventListener("drop", function (event) {
  event.preventDefault();
  fileUploadContainer.classList.remove("dragover");
  fileInput.files = event.dataTransfer.files; // Set dropped files to the input
  handleFiles(); // Process the files
});

// Function to display selected or dropped files
function handleFiles() {
  const files = fileInput.files;
  fileList.innerHTML = ""; // Clear previous file list

  for (let i = 0; i < files.length; i++) {
    const file = files[i];

    console.log(`File Name: ${file}`);
    console.log(`File Type: ${file.type}`);
    console.log(`File Size: ${file.size} bytes`);
    console.log(
      `Last Modified: ${new Date(file.lastModified).toLocaleString()}`
    );

    const reader = new FileReader();
    reader.onload = function (event) {
      const fileContent = event.target.result;
    };
    reader.readAsText(file);
    const li = document.createElement("li");
    li.textContent = files[i].name;
    fileList.appendChild(li);
  }
}
