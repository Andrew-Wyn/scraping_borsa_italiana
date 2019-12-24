// Get the input field
var input = document.getElementById("search");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {

  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("search_btn").click();
  }
});

function go() {
    document.location.href = "http://127.0.0.1:5000/borsa?term=" + input.value
}