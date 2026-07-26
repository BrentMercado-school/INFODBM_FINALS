async function loadMyItems() {
    const message = document.getElementById("table_message");
    const grid = document.getElementById("my_items_grid");

    const filter = document.getElementById("item_filter").value;
    const search = document.getElementById("item_search").value.trim();

    message.textContent = "Loading items...";
    grid.innerHTML = "";

    const parameters = new URLSearchParams({ filter: filter, search: search });

    try {
        const res = await fetch(`/api/items/my-items?${parameters.toString()}`);
        const data = await res.json();

        if (!res.ok) {
            message.textContent = data.error || "Unable to load items.";
            return;
        }
        if (data.length === 0) {
            message.textContent = search
                ? "No matching items found."
                : "You have not added any items yet.";
            return;
        }

        message.textContent = "";

        data.forEach(item => {
            const imageHTML = item.image
                ? `<img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.name)}">`
                : `<div class="card-noimage">No image</div>`;

            // status pill color
            let statusClass = "status-available";
            if (item.status === "Borrowed") statusClass = "status-borrowed";
            else if (item.status === "Unavailable") statusClass = "status-returned";

            // actions: disabled if borrowed
            const actions = item.status === "Borrowed"
                ? `<button class="btn-accept" onclick="returnItem(${item.borrow_form_id})">Return</button>`
                : `<button class="btn-accept" onclick="openEditItemModal(${item.id})">Edit</button>
                   <button class="btn-decline" onclick="softDeleteItem(${item.id})">Delete</button>`;

            grid.innerHTML += `
                <div class="item-card">
                    <div class="card-image">${imageHTML}</div>
                    <div class="card-body">
                        <div class="card-top-row">
                            <h3 class="card-title">${escapeHtml(item.name)}</h3>
                            <span class="status-pill ${statusClass}">${escapeHtml(item.status)}</span>
                        </div>
                        <p class="card-category">${escapeHtml(item.category)}</p>
                        <p class="card-meta">Condition: ${escapeHtml(item.condition)}</p>
                        <p class="card-meta">Deposit: ₱${Number(item.security_deposit).toFixed(2)}</p>
                        <p class="card-date">Added ${escapeHtml(item.created_at || "—")}</p>
                        <div class="card-actions">${actions}</div>
                    </div>
                </div>
            `;
        });

        lucide.createIcons();
    } catch (error) {
        console.error("LOAD MY ITEMS ERROR:", error);
        message.textContent = "Unable to load items.";
    }
}

async function softDeleteItem(itemID) {
   const confirmed = confirm(
       "Are you sure you want to delete this item?"
   );


   if (!confirmed) {
       return;
   }


   const message = document.getElementById("table_message");


   try {
       const res = await fetch(`/api/items/${itemID}`, {
           method: "DELETE"
       });


       const data = await res.json();


       if (!res.ok) {
           message.textContent =
               data.error || "Unable to delete item.";
           return;
       }


       await loadMyItems();


       message.textContent = data.message;


   } catch (error) {
       console.error("SOFT DELETE ITEM ERROR:", error);
       message.textContent = "Unable to delete item.";
   }
}

function escapeHtml(value) {
   return String(value)
       .replaceAll("&", "&amp;")
       .replaceAll("<", "&lt;")
       .replaceAll(">", "&gt;")
       .replaceAll('"', "&quot;")
       .replaceAll("'", "&#039;");
}

let selectedItemID = null;

async function openEditItemModal(itemID) {
   const message = document.getElementById("edit_item_message");


   message.textContent = "Loading item...";


   try {
       const res = await fetch(`/api/my-items/${itemID}`);
       const item = await res.json();


       if (!res.ok) {
           message.textContent =
               item.error || "Unable to load item.";
           return;
       }


       if (item.status === "Borrowed") {
           document.getElementById("table_message").textContent =
               "A borrowed item cannot be edited.";
           return;
       }


       selectedItemID = item.id;


       await loadEditCategories(item.category_id);


       document.getElementById("edit_item_name").value =
           item.name || "";


       document.getElementById("edit_condition").value =
           item.condition || "";


       document.getElementById("edit_description").value =
           item.description || "";


       document.getElementById("edit_note").value =
           item.note || "";


       document.getElementById("edit_security_deposit").value =
           item.security_deposit || 0;


       document.getElementById("edit_image").value = "";


       message.textContent = "";


       document.getElementById("edit_item_modal").style.display =
           "flex";


   } catch (error) {
       console.error("LOAD ITEM ERROR:", error);
       message.textContent = "Unable to load item.";
   }
}

async function loadEditCategories(selectedCategoryID) {
   const select = document.getElementById("edit_category");


   select.innerHTML =
       `<option value="">Select a category</option>`;


   const res = await fetch("/api/categories");
   const data = await res.json();


   if (!res.ok) {
       throw new Error(
           data.error || "Unable to load categories."
       );
   }


   data.forEach(category => {
       const option = document.createElement("option");


       option.value = category.id;
       option.textContent = category.name;


       if (Number(category.id) === Number(selectedCategoryID)) {
           option.selected = true;
       }


       select.appendChild(option);
   });
}

async function updateItem() {
   if (selectedItemID === null) {
       return;
   }


   const message = document.getElementById("edit_item_message");


   const itemName =
       document.getElementById("edit_item_name").value.trim();


   const category =
       document.getElementById("edit_category").value;


   const condition =
       document.getElementById("edit_condition").value.trim();


   const description =
       document.getElementById("edit_description").value.trim();


   const note =
       document.getElementById("edit_note").value.trim();


   const securityDeposit =
       document.getElementById(
           "edit_security_deposit"
       ).value || 0;


   const image =
       document.getElementById("edit_image").files[0];


   if (!itemName || !category || !condition) {
       message.textContent =
           "Please fill in the item name, category, and condition.";
       return;
   }


   if (Number(securityDeposit) < 0) {
       message.textContent =
           "Security deposit cannot be negative.";
       return;
   }


   const formData = new FormData();


   formData.append("item_name", itemName);
   formData.append("category", category);
   formData.append("condition", condition);
   formData.append("description", description);
   formData.append("note", note);
   formData.append("security_deposit", securityDeposit);


   if (image) {
       formData.append("image", image);
   }


   try {
       const res = await fetch(
           `/api/items/${selectedItemID}`,
           {
               method: "PUT",
               body: formData
           }
       );


       const data = await res.json();


       if (!res.ok) {
           message.textContent =
               data.error || "Unable to update item.";
           return;
       }


       cancelEdit();


       await loadMyItems();


       document.getElementById("table_message").textContent =
           data.message;


   } catch (error) {
       console.error("UPDATE ITEM ERROR:", error);
       message.textContent = "Unable to update item.";
   }
}

function cancelEdit() {
   selectedItemID = null;


   document.getElementById("edit_item_name").value = "";
   document.getElementById("edit_category").value = "";
   document.getElementById("edit_condition").value = "";
   document.getElementById("edit_description").value = "";
   document.getElementById("edit_note").value = "";
   document.getElementById("edit_security_deposit").value = "";
   document.getElementById("edit_image").value = "";
   document.getElementById("edit_item_message").textContent = "";


   document.getElementById("edit_item_modal").style.display =
       "none";
}

function searchItems() {
   loadMyItems();
}

function clearSearch() {
   document.getElementById("item_search").value = "";
   loadMyItems();
}

document
   .getElementById("item_search")
   .addEventListener("keydown", function (event) {
       if (event.key === "Enter") {
           searchItems();
       }
   });

function setFilter(value) {
    document.getElementById("item_filter").value = value;

    document.querySelectorAll(".filter-chips .chip").forEach(chip => {
        chip.classList.toggle("active", chip.dataset.filter === value);
    });

    loadMyItems();
}

async function logout() {
    const res = await fetch("/api/logout", { method: "POST" });
    if (res.ok) window.location.href = "/";
}

let returnBorrowFormId = null;

async function returnItem(borrowFormId) {
    returnBorrowFormId = borrowFormId;

    try {
        const res = await fetch(`/api/return_details/${borrowFormId}`);
        const data = await res.json();

        if (!res.ok) {
            document.getElementById("table_message").textContent = data.error;
            return;
        }

        // borrower
        setImage("borrower_image", data.borrower_image);
        document.getElementById("borrower_name").textContent = data.borrower_name;
        document.getElementById("borrower_email").textContent = data.borrower_email || "";
        document.getElementById("borrower_address").textContent = data.borrower_address || "Not set";

        // item
        setImage("return_item_image", data.item_image);
        document.getElementById("return_item_name").textContent = data.item_name;
        document.getElementById("return_item_category").textContent = data.item_category;
        document.getElementById("return_item_condition").textContent = data.item_condition;
        document.getElementById("return_item_deposit_text").textContent = data.security_deposit.toFixed(2);

        // read-only fields
        document.getElementById("return_start_date").value = data.start_date;
        document.getElementById("return_expected_date").value = data.expected_return;
        document.getElementById("return_security_deposit").value = "₱" + data.security_deposit.toFixed(2);

        // reset editable
        document.getElementById("return_actual_date").value = "";
        document.getElementById("return_damage_fee").value = "";
        document.getElementById("return_modal_message").textContent = "";

        document.getElementById("return_modal").style.display = "flex";
        lucide.createIcons();
    } catch (error) {
        console.error("RETURN DETAILS ERROR:", error);
        document.getElementById("table_message").textContent = "Unable to load return details.";
    }
}

function setImage(id, url) {
    const img = document.getElementById(id);
    if (url) {
        img.src = url;
        img.style.display = "block";
    } else {
        img.style.display = "none";
    }
}

function closeReturnModal() {
    document.getElementById("return_modal").style.display = "none";
    returnBorrowFormId = null;
}

loadMyItems();



