
async function logout()
{
    const res  = await  fetch("/api/logout",  {method: 'POST'})

    if (res.ok) {
        window.location.href = "/"
    }
}
async function addItem()
{
    const item_name = document.getElementById("item_name").value;
    const category = document.getElementById("category").value;
    const condition = document.getElementById("condition").value;
    const description = document.getElementById("description").value;
    const note = document.getElementById("note").value;
    const security_deposit = document.getElementById("security_deposit").value || 0;
    const image = document.getElementById("image").files[0];

    if (!item_name || !category || !condition){
        document.getElementById("add_item_message").textContent =
            "Please fill in the item name, category, and condition.";
        return;
    }

    const formData = new FormData();
    formData.append("item_name", item_name);
    formData.append("category", category);
    formData.append("condition", condition);
    formData.append("description", description);
    formData.append("note", note);
    formData.append("security_deposit", security_deposit);
    if (image) {
        formData.append("image", image);
    }

    const res = await fetch("/api/items/add", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (res.ok) {
        document.getElementById("item_name").value = "";
        document.getElementById("category").value = "";
        document.getElementById("condition").value = "";
        document.getElementById("description").value = "";
        document.getElementById("note").value = "";
        document.getElementById("security_deposit").value = "";
        document.getElementById("image").value = "";

        document.getElementById("general_message").textContent = data.message;
        document.getElementById("add_item_modal").style.display = "none";
    }  else {
        document.getElementById("add_item_message").textContent = data.error;

    }
}
function openAddItemModal()
{
    document.getElementById("add_item_modal").style.display = "block";
    loadCategories()
}
function cancelAdd()
{

    document.getElementById("item_name").value = "";
    document.getElementById("category").value = "";
    document.getElementById("condition").value = "";
    document.getElementById("description").value = "";
    document.getElementById("note").value = "";
    document.getElementById("security_deposit").value = "";
    document.getElementById("image").value = "";

    document.getElementById("add_item_modal").style.display = "none";
}
async function loadCategories()
{
    const res = await fetch("/api/categories");
    const data = await res.json();
    const select =  document.getElementById("category");
    select.innerHTML = "";

    if (res.ok) {
        select.innerHTML = `<option value="">Select a category</option>>`
        data.forEach(c =>  {
            select.innerHTML  += `
            <option value="${c.id}">${c.name}</option>;
            `
        });
    } else {
        document.getElementById("general_message").textContent = data.error;
    }
}
async function loadCommunityItems()
{
    const res = await fetch ("/api/items/community_items");
    const data = await res.json();
    const tbody = document.querySelector("#community_items_table tbody");
    tbody.innerHTML  = "";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }

    if (data.length === 0) {
        document.getElementById("table_message").textContent = "No community items found.";
        return;
    }

    data.forEach(i => {
        tbody.innerHTML += `
            <tr>
                <td>${i.image ? `<img src="${i.image}" alt="" style="width:48px;height:48px;object-fit:cover;">`: "No image"}</td>
                <td>${i.name}</td>
                <td>${i.category}</td>
                <td>${i.condition}</td>
                <td>${i.owner}</td>
                <td>₱${i.security_deposit}</td>
                <td>${i.status}</td>
                <td>
                    <button onclick="viewItemDetails(${i.id})">VIEW</button>
                </td> 
            </tr>
        `;
    });
}
loadCommunityItems()