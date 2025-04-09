document.getElementById("signupForm").addEventListener("submit", function (e) {
    const password = document.getElementById("id_password").value;
    const confirmPassword = document.getElementById("id_confirm_password").value;

    if (password !== confirmPassword) {
        e.preventDefault();
        alert("Passwords do not match!");
    }
});
