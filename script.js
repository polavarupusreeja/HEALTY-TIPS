
function loginUser() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    
    if (username === "admin" && password === "1234") {
        alert("Login Successful!");
        window.location.href = "details.html";
    } else {
        alert("Invalid Username or Password!");
    }
    return false;
}


