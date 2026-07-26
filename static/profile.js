async function loadProfile() {
    const res = await fetch("/api/profile");
    const data = await res.json();

    if (!res.ok) {
        document.getElementById("general_message").textContent = data.error;
        return;
    }

    document.getElementById("display_username").textContent = data.username;

    document.getElementById("display_address").textContent = data.address || "Not set";
    document.getElementById("display_contact").textContent = data.contact || "Not set";

    if (data.image) {
        const img = document.getElementById("profile_image");
        img.src = data.image;
        img.style.display = "block";
        document.getElementById("profile_placeholder").style.display = "none";
    }
}

function openEditProfileModal() {
    document.getElementById("edit_username").value =
        document.getElementById("display_username").textContent;

    const address = document.getElementById("display_address").textContent;
    const contact = document.getElementById("display_contact").textContent;

    document.getElementById("edit_address").value = address === "Not set" ? "" : address;
    document.getElementById("edit_contact").value = contact === "Not set" ? "" : contact;

    document.getElementById("edit_message").textContent = "";
    document.getElementById("edit_profile_modal").style.display = "flex";
}

function closeEditProfileModal() {
    document.getElementById("edit_profile_modal").style.display = "none";
}

async function saveProfile() {
    const username = document.getElementById("edit_username").value;
    const address = document.getElementById("edit_address").value;
    const contact = document.getElementById("edit_contact").value;
    const image = document.getElementById("edit_image").files[0];

    if (!username) {
        document.getElementById("edit_message").textContent = "Username cannot be empty.";
        return;
    }

    const formData = new FormData();
    formData.append("username", username);
    formData.append("address", address);
    formData.append("contact", contact);
    if (image) {
        formData.append("image", image);
    }

    const res = await fetch("/api/profile/update", {
        method: "PUT",
        body: formData
    });

    const data = await res.json();

    if (res.ok) {
        closeEditProfileModal();
        document.getElementById("edit_image").value = "";
        document.getElementById("general_message").textContent = data.message;
        loadProfile();
    } else {
        document.getElementById("edit_message").textContent = data.error;
    }
}

async function logout() {
    const res = await fetch("/api/logout", { method: "POST" });
    if (res.ok) window.location.href = "/";
}

async function loadStats() {
    const res = await fetch("/api/profile/stats");
    const data = await res.json();

    if (!res.ok) return;

    document.getElementById("stat_shared").textContent = data.items_shared;
    document.getElementById("stat_lent").textContent = data.items_lent_out;
    document.getElementById("stat_borrowing").textContent = data.items_borrowing;
    document.getElementById("stat_completed").textContent = data.borrows_completed;
}

loadProfile();
loadStats();
