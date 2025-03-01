document
  .getElementById("num_flash_cards")
  .addEventListener("input", function (event) {
    this.value = this.value.replace(/[^0-9]/g, ""); // Remove non-numeric characters
  });

const form = document.getElementById("form");

form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevents the default form submission

  // Collect the values from the input fields
  //  const course = document.getElementById("course_name").value;
  //const subject = document.getElementById("subject").value;
  //const rules = document.getElementById("rules").value;
  //const num_flash_cards = document.getElementById("num_flash_cards").value;
  //const difficulty = document.getElementById("difficulty").value;
  //const education = document.getElementById("school_level").value;
  //const file = document.getElementById('subject_material').value;

  // Display the collected data (or use it for further processing)
  //const response = `
  //      Course: ${course}
  //      Subject: ${subject}
  //      Rules: ${rules}
  //      Number of Flash Cards: ${num_flash_cards}
  //      Difficulty: ${difficulty}
  //      Education Level: ${education}
  //      File:
  //  `;

  form.submit();
  console.log(response);
});
