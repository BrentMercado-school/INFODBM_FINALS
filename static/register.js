async function registerUser()
{
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const msg = document.getElementById("error_message");

    if (!password || !username)
    {
        msg.style.color = "#d32f2f";
        msg.textContent = "Please enter a username and password.";
        return;
    }

    const res = await fetch("/api/auth/register", {
       method: "POST",
       headers: {"Content-Type": "application/json"},
       body: JSON.stringify({
           username, password
       })
   });

    const data = await res.json()

    if (res.ok)
     {
        msg.style.color = "green";
        msg.textContent = data.message;

        document.getElementById("username").value = "";
        document.getElementById("password").value = "";

    } else {
        msg.style.color = "#d32f2f";
        msg.textContent = data.error;
    }
}

async function loginUser()
{
    const username = document.getElementById("username_login").value;
    const password = document.getElementById("password_login").value;
    const msg = document.getElementById("error_message_login");

    if (!username || !password) {
        msg.style.color = "#d32f2f";
        msg.textContent = "Please enter your username and password.";
        return;
    }

    const res  = await fetch("/api/auth/login", {
       method: "POST",
       headers: {"Content-Type": "application/json"},
       body: JSON.stringify({
           username, password
       })
   });

    const data = await res.json();

    if (res.ok) {
        document.getElementById("username_login").value = "";
        document.getElementById("password_login").value = "";

        msg.style.color = "green";
        msg.textContent = data.message;

        window.location.href = "/api/home";
    } else {
        msg.style.color = "#d32f2f";
        msg.textContent = data.error;
    }
}
function showLogin() {
    document.getElementById("register_box").classList.remove("active");
    document.getElementById("login_box").classList.add("active");
}

function showRegister() {
    document.getElementById("login_box").classList.remove("active");
    document.getElementById("register_box").classList.add("active");
}