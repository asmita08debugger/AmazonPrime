function loginUser() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    if (email === "" || password === "") {
        alert("Please enter your email and password.");
        return;
    }

    alert("Sign in successful!");
    window.location.href = "index.html";
}


function signupUser() {
    const name = document.getElementById("signupName").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (name === "" || email === "" || password === "" || confirmPassword === "") {
        alert("Please fill in all fields.");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    alert("Account created successfully!");
    window.location.href = "login.html";
}
function watchNow() {
    alert("Starting The Tomorrow War...");
}


function showMovieInfo() {
    alert("The Tomorrow War\n\nAction • Science Fiction\n\nA Prime Video Original.");
}


function selectMovie(title) {
    alert("You selected: " + title);
}