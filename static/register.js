async function registerUser()
{
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!password)
    {
        document.getElementById("error_message").textContent = "Please enter a password.";
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
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
        document.getElementById("error_message").textContent = data.message;

    } else {
        document.getElementById("error_message").textContent = data.error;
    }
}

async function loginUser()
{
    const username = document.getElementById("username_login").value;
    const password = document.getElementById("password_login").value;

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
        document.getElementById("error_message").textContent = data.message;

        window.location.href = "/api/home";
    } else {
        document.getElementById("error_message").textContent = data.error;
    }
}