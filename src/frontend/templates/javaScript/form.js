document.getElementById("num_flash_cards").addEventListener("input", function (event) {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
});

document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevents the default form submission

    // Collect the values from the input fields
    const course = document.getElementById('course_name').value;
    const subject = document.getElementById('subject').value;
    const rules = document.getElementById('rules').value;
    const num_flash_cards = document.getElementById('num_flash_cards').value;
    const difficulty = document.getElementById('difficulty').value;
    const education = document.getElementById('school_level').value;

    // Display the collected data (or use it for further processing)
    const response = `
        Course: ${course}
        Subject: ${subject}
        Rules: ${rules}
        Number of Flash Cards: ${num_flash_cards}
        Difficulty: ${difficulty}
        Education Level: ${education}
        File: ${fileInput}
    `;
    console.log(response);
});

const fileInput = document.getElementById('fileInput');
const fileUploadContainer = document.getElementById('fileUploadContainer');
const fileList = document.getElementById('fileList');

// Handle file selection (either via button or drag-and-drop)
fileInput.addEventListener('change', handleFiles);

// Handle drag-over event (needed to allow dropping files)
fileUploadContainer.addEventListener('dragover', function(event) {
    event.preventDefault();
    fileUploadContainer.classList.add('dragover');
});

// Handle drag-leave event
fileUploadContainer.addEventListener('dragleave', function(event) {
    fileUploadContainer.classList.remove('dragover');
});

// Handle drop event (files being dropped)
fileUploadContainer.addEventListener('drop', function(event) {
    event.preventDefault();
    fileUploadContainer.classList.remove('dragover');
    fileInput.files = event.dataTransfer.files;  // Set dropped files to the input
    handleFiles(); // Process the files
});

// Function to display selected or dropped files
function handleFiles() {
    const files = fileInput.files;
    fileList.innerHTML = '';  // Clear previous file list

    for (let i = 0; i < files.length; i++) {
        const li = document.createElement('li');
        li.textContent = files[i].name;
        fileList.appendChild(li);
    }
}