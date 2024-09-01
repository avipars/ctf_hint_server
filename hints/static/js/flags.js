document.getElementById("resetButton").addEventListener("click", function(event) {
    let confirmAction = confirm("Are you sure you want to reset your progress? This action cannot be undone.");
    
    if (!confirmAction) {
        event.preventDefault(); // Prevent form submission if the user cancels
    }
});