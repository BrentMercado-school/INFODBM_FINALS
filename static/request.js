async function loadAllBorrowRequest() {
    setActiveRequestChip("All");

    const res = await fetch("/api/borrow_request/all");
    const data = await res.json();
    const list = document.getElementById("request_list");
    list.innerHTML = "";

    document.getElementById("request_header").textContent = "All Requests";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }
    if (data.length === 0) {
        document.getElementById("table_message").textContent = "No pending requests.";
        return;
    }

    document.getElementById("table_message").textContent = "";

    data.forEach(d => {
        const imageHTML = d.image
            ? `<img src="${d.image}" alt="${d.name}">`
            : `<div class="req-noimage">No image</div>`;

        list.innerHTML += `
            <div class="request-card">
                <div class="request-top">
                    <div class="request-image">${imageHTML}</div>

                    <div class="request-info">
                        <h3 class="request-title">${d.name}</h3>
                        <p class="request-category">${d.category}</p>

                        <div class="request-dates">
                            <p><span class="date-label">Start Date:</span> ${d.start_date}</p>
                            <p><span class="date-label">Return Date:</span> ${d.return_date}</p>
                        </div>

                        <p class="request-deposit">Deposit: ₱${d.security_deposit}</p>

                        <div class="request-borrower">
                            <span>${d.owner}</span>
                        </div>
                    </div>
                </div>

                <div class="request-actions">
                    <button class="btn-accept" onclick="acceptBorrowRequest(${d.borrow_form_id}, ${d.item_id})">Accept</button>
                    <button class="btn-decline" onclick="openDeclineRequestModal(${d.borrow_form_id})">Decline</button>
                    <button class="btn-details">Details</button>
                </div>
            </div>
        `;
    });
}

async function loadMyBorrowRequest() {
    setActiveRequestChip("My Borrow Request");

    const res = await fetch("/api/my_borrow_request");
    const data = await res.json();
    const list = document.getElementById("request_list");
    list.innerHTML = "";

    document.getElementById("request_header").textContent = "My Borrow Requests";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }
    if (data.length === 0) {
        document.getElementById("table_message").textContent = "You haven't made any borrow requests.";
        return;
    }

    document.getElementById("table_message").textContent = "";

    data.forEach(d => {
    const imageHTML = d.image
        ? `<img src="${d.image}" alt="${d.name}">`
        : `<div class="req-noimage">No image</div>`;

    let statusClass = "status-pending";
    if (d.status === "Accepted") statusClass = "status-accepted";
    else if (d.status === "Declined") statusClass = "status-declined";
    else if (d.status === "Cancelled") statusClass = "status-declined";

    // Only show the Cancel button when the request is still Pending
    const cancelButton = d.status === "Pending"
        ? `<div class="request-actions">
               <button class="btn-decline" onclick="cancelBorrowRequest(${d.borrow_form_id})">Cancel Request</button>
           </div>`
        : "";

    list.innerHTML += `
        <div class="request-card">
            <div class="request-top">
                <div class="request-image">${imageHTML}</div>

                <div class="request-info">
                    <h3 class="request-title">${d.name}</h3>
                    <p class="request-category">${d.category}</p>

                    <div class="request-dates">
                        <p><span class="date-label">Start Date: ${d.start_date}</p>
                        <p><span class="date-label">Return Date: ${d.return_date}</p>
                    </div>

                    <p class="request-deposit">Deposit: ₱${d.security_deposit}</p>

                    <div class="request-status-row">
                        <span class="status-pill ${statusClass}">${d.status}</span>
                    </div>
                </div>
            </div>
            ${cancelButton}
        </div>
    `;
});
}

async function acceptBorrowRequest(borrow_form_id, item_id)
{
    const res = await fetch ("/api/borrow_request/accept", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({borrow_form_id, item_id})
    })

    const data = await res.json();

    if (res.ok) {
        document.getElementById("general_message").textContent = data.message

        loadAllBorrowRequest();
    } else {
        document.getElementById("general_message").textContent = data.error;
    }
}

async function openDeclineRequestModal(borrow_form_id)
{
    document.getElementById("decline_modal").style.display = "flex";
    document.getElementById("borrow_form_id").value = borrow_form_id;
}

async function closeDeclineRequestModal()
{
    document.getElementById("decline_modal").style.display = "none";
    document.getElementById("decline_reason").value = "";
}

async function declineBorrowRequest()
{
    const decline_reason = document.getElementById("decline_reason").value;
    const borrow_form_id = document.getElementById("borrow_form_id").value;

    const res  = await  fetch ("/api/borrow_request/decline", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({decline_reason, borrow_form_id})
    })

    const data = await res.json();

    if (res.ok) {
        document.getElementById("general_message").textContent = data.message

        closeDeclineRequestModal()
        loadAllBorrowRequest();
    }  else {
        document.getElementById("general_message").textContent = data.error;
    }
}
function setActiveRequestChip(label) {
    document.querySelectorAll(".filter-chips .chip").forEach(chip => {
        if (chip.textContent.trim() === label) {
            chip.classList.add("active");
        } else {
            chip.classList.remove("active");
        }
    });
}
async function logout() {
    const res = await fetch("/api/logout", { method: "POST" });
    if (res.ok) window.location.href = "/";
}

async function cancelBorrowRequest(borrow_form_id) {
    if (!confirm("Cancel this borrow request?")) return;

    const res = await fetch(`/api/my_borrow_request/cancel/${borrow_form_id}`, {
        method: "PUT"
    });

    const data = await res.json();

    if (res.ok) {
        document.getElementById("general_message").textContent = data.message;
        loadMyBorrowRequest();   // refresh the list
    } else {
        document.getElementById("general_message").textContent = data.error;
    }
}

async function loadOngoingBorrowRequest() {
    setActiveRequestChip("Ongoing");

    const res = await fetch("/api/ongoing_borrow_request");
    const data = await res.json();
    const list = document.getElementById("request_list");
    list.innerHTML = "";

    document.getElementById("request_header").textContent = "Ongoing Borrowed Items";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }
    if (data.length === 0) {
        document.getElementById("table_message").textContent = "No ongoing borrowed items.";
        return;
    }

    document.getElementById("table_message").textContent = "";

    data.forEach(d => {
        const imageHTML = d.image
            ? `<img src="${d.image}" alt="${d.name}">`
            : `<div class="req-noimage">No image</div>`;

        // color the status pill by the function's result
        let statusClass = "status-ontrack";
        if (d.status === "Due Today") statusClass = "status-duetoday";
        else if (d.status === "Overdue") statusClass = "status-overdue";

        list.innerHTML += `
            <div class="request-card">
                <div class="request-top">
                    <div class="request-image">${imageHTML}</div>

                    <div class="request-info">
                        <h3 class="request-title">${d.name}</h3>
                        <p class="request-category">${d.category}</p>

                        <div class="request-dates">
                            <p><span class="date-label">Start Date:</span> ${d.start_date}</p>
                            <p><span class="date-label">Return Date:</span> ${d.return_date}</p>
                        </div>

                        <p class="request-deposit">Deposit: ₱${d.security_deposit}</p>

                        <div class="request-status-row">
                            <span class="status-pill ${statusClass}">${d.status}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

async function loadHistoryBorrowRequest() {
    setActiveRequestChip("History");

    const res = await fetch("/api/history_borrow_request");
    const data = await res.json();
    const list = document.getElementById("request_list");
    list.innerHTML = "";

    document.getElementById("request_header").textContent = "Borrow History";

    if (!res.ok) {
        document.getElementById("table_message").textContent = data.error;
        return;
    }
    if (data.length === 0) {
        document.getElementById("table_message").textContent = "No borrow history yet.";
        return;
    }

    document.getElementById("table_message").textContent = "";

    data.forEach(d => {
        const imageHTML = d.image
            ? `<img src="${d.image}" alt="${d.name}">`
            : `<div class="req-noimage">No image</div>`;

        list.innerHTML += `
            <div class="request-card">
                <div class="request-top">
                    <div class="request-image">${imageHTML}</div>

                    <div class="request-info">
                        <h3 class="request-title">${d.name}</h3>
                        <p class="request-category">${d.category}</p>

                        <div class="request-dates">
                            <p><span class="date-label">Start Date:</span> ${d.start_date}</p>
                            <p><span class="date-label">Return Date:</span> ${d.return_date}</p>
                        </div>

                        <p class="request-deposit">Deposit: ₱${d.security_deposit}</p>

                        <div class="request-status-row">
                            <span class="status-pill status-returned">Returned</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}
loadAllBorrowRequest();