// ---------- Build one item card ----------
function buildItemCard(i) {
    let statusHTML;
    if (i.status === "Available") {
        statusHTML = `
            <div class="card-status available">
                <i data-lucide="check-circle"></i>
                <span>available</span>
            </div>`;
    } else {
        statusHTML = `
            <div class="card-status borrowed">
                <i data-lucide="clock"></i>
                <span>${i.status}</span>
            </div>`;
    }

    const imageHTML = i.image
        ? `<img src="${i.image}" alt="${i.name}">`
        : `<div class="card-noimage">No image</div>`;

    return `
        <div class="item-card" onclick="openViewItemDetailsModal(${i.id})">
            <div class="card-image">${imageHTML}</div>
            <div class="card-body">
                <h3 class="card-title">${i.name}</h3>
                <div class="card-owner"><span>${i.owner}</span></div>
                ${statusHTML}
            </div>
        </div>
    `;
}

// ---------- Shared renderer ----------
// Takes a URL, fetches it, and draws the cards
async function renderItems(url) {
    const res = await fetch(url);
    const data = await res.json();
    const grid = document.getElementById("community_items_grid");
    grid.innerHTML = "";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }
    if (data.length === 0) {
        document.getElementById("table_message").textContent = "No items found.";
        return;
    }

    document.getElementById("table_message").textContent = "";
    data.forEach(i => grid.innerHTML += buildItemCard(i));
    lucide.createIcons();   // render icons on the new cards
}

// ---------- Category loaders (match your API routes) ----------
function loadAllCommunityItems() {
    setActiveChip("All Items");
    renderItems("/api/items/community_items/all");
}
function loadApplianceCommunityItems() {
    setActiveChip("Appliance");
    renderItems("/api/items/community_items/appliance");
}
function loadTechnologyCommunityItems() {
    setActiveChip("Technology");
    renderItems("/api/items/community_items/technology");
}
function loadSportsCommunityItems() {
    setActiveChip("Sports");
    renderItems("/api/items/community_items/sports");
}

// ---------- Search ----------
function loadSearchCommunityItems() {
    const search = document.getElementById("search_item").value.trim();
    if (!search) {
        loadAllCommunityItems();
        return;
    }
    document.getElementById("filtered_by").textContent = `Search results for: "${search}"`;
    // also clear active chips since none apply to a search
    document.querySelectorAll(".chip").forEach(chip => chip.classList.remove("active"));
    renderItems(`/api/items/community_items/search/${encodeURIComponent(search)}`);
}

// ---------- Highlight the active chip ----------
function setActiveChip(label) {
    document.querySelectorAll(".chip").forEach(chip => {
        if (chip.textContent.trim() === label) {
            chip.classList.add("active");
        } else {
            chip.classList.remove("active");
        }
    });
}

// ---------- View item modal ----------
async function openViewItemDetailsModal(id) {
    const res = await fetch(`/api/items/${id}`);
    const data = await res.json();

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }

    document.getElementById("view_item_modal").style.display = "flex";

    // reset to default state each time
    document.getElementById("view_details_buttons").style.display = "flex";
    document.getElementById("borrow_details_modal").style.display = "none";
    document.getElementById("borrow_message").textContent = "";
    document.getElementById("start_date").value = "";
    document.getElementById("return_date").value = "";

    // image
    if (data["image"]) {
        document.getElementById("item_image_borrow").src = data["image"];
        document.getElementById("item_image_borrow").style.display = "";
    } else {
        document.getElementById("item_image_borrow").style.display = "none";
    }

    // fill fields
    document.getElementById("item_id").value = data["id"];
    document.getElementById("item_name_borrow").value = data["name"];
    document.getElementById("item_name_category").value = data["category"];
    document.getElementById("item_name_condition").value = data["condition"];
    document.getElementById("item_owner").value = data["owner"];
    document.getElementById("item_security_deposit").value = data["security_deposit"];
    document.getElementById("item_security_status").value = data["status"];
    document.getElementById("item_note_borrow").value = data["note"];
}

function closeViewItemDetailsModal() {
    document.getElementById("view_item_modal").style.display = "none";
}

// ---------- Borrow flow ----------
function openBorrowDetailsModal() {
    const status = document.getElementById("item_security_status").value;

    if (status === "Borrowed" || status === "Unavailable") {
        document.getElementById("borrow_message").textContent = "Item cannot be borrowed";
        return;
    }
    document.getElementById("view_details_buttons").style.display = "none";
    document.getElementById("borrow_details_modal").style.display = "block";
}

function cancelBorrow() {
    document.getElementById("borrow_details_modal").style.display = "none";
    document.getElementById("view_details_buttons").style.display = "flex";
    document.getElementById("borrow_message").textContent = "";
    document.getElementById("start_date").value = "";
    document.getElementById("return_date").value = "";
}

async function borrowItem() {
    const item_id = document.getElementById("item_id").value;
    const startDate = document.getElementById("start_date").value;
    const returnDate = document.getElementById("return_date").value;

    if (!startDate || !returnDate) {
        document.getElementById("borrow_message").textContent = "Please select both dates.";
        return;
    }
    if (returnDate < startDate) {
        document.getElementById("borrow_message").textContent = "Return date must be on or after the start date.";
        return;
    }

    const res = await fetch(`/api/borrowItem/${item_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ startDate, returnDate })
    });
    const data = await res.json();

    if (res.ok) {
        closeViewItemDetailsModal();
        loadAllCommunityItems();
    } else {
        document.getElementById("borrow_message").textContent = data.error;
    }
}

// ---------- Logout ----------
async function logout() {
    const res = await fetch("/api/logout", { method: "POST" });
    if (res.ok) {
        window.location.href = "/";
    }
}

// ---------- Search on Enter key ----------
document.getElementById("search_item").addEventListener("keypress", function(e) {
    if (e.key === "Enter") loadSearchCommunityItems();
});

function setActiveChip(label) {
    // highlight the active chip
    document.querySelectorAll(".chip").forEach(chip => {
        if (chip.textContent.trim() === label) {
            chip.classList.add("active");
        } else {
            chip.classList.remove("active");
        }
    });

    // update the "Filtered by" label
    document.getElementById("filtered_by").textContent = "Filtered by: " + label;
}
// Read the URL query parameters when the page loads
function handleUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const category = params.get("category");   // e.g. "appliance"
    const focus = params.get("focus");          // e.g. "search"

    // If a category was passed, load that filter
    if (category === "appliance") {
        loadApplianceCommunityItems();
    } else if (category === "technology") {
        loadTechnologyCommunityItems();
    } else if (category === "sports") {
        loadSportsCommunityItems();
    } else {
        loadAllCommunityItems();   // default / "all"
    }

    // If the user clicked search on the home page, focus the search box
    if (focus === "search") {
        document.getElementById("search_item").focus();
    }
}

// Run this instead of a plain loadAllCommunityItems()
handleUrlParams();