document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#dataTable tbody');
    const addButton = document.getElementById('addServiceTypeButton');
    const nameInput = document.getElementById('name');
    const descriptionInput = document.getElementById('description');
    // Retrieve the access token from sessionStorage
    const accessToken = sessionStorage.getItem('access');
    if (!accessToken) {
        console.error('Access token not found. Please log in.');
        window.location.href = 'login.html';
        return;
    }
    // Function to load table data
    async function loadServiceTypes() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/service/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                const serviceTypes = await response.json();
                tableBody.innerHTML = '';
                serviceTypes.forEach(service => {
                    const row = document.createElement("tr");
                    // Create columns
                    const nameCell = document.createElement("td");
                    const descriptionCell = document.createElement("td");
                    const editCell = document.createElement("td");
                    const deleteCell = document.createElement("td");
                    const editButton = document.createElement("a");
                    const deleteButton = document.createElement("a");
                    // Configure edit and delete buttons
                    editButton.classList = "btn btn-primary";
                    editButton.innerHTML = 'Edit';
                    deleteButton.classList = "btn btn-danger";
                    deleteButton.innerHTML = 'Delete';
                    // Fill cells with data
                    nameCell.textContent = service.name;
                    descriptionCell.textContent = service.description;
                    editCell.appendChild(editButton)
                    deleteCell.appendChild(deleteButton)
                    // Append cells to row
                    row.appendChild(nameCell);
                    row.appendChild(descriptionCell);
                    row.appendChild(editCell);
                    row.appendChild(deleteCell);
                    // Append row to table body
                    tableBody.appendChild(row);
                });
                if (tableBody.innerHTML === '') {

                }
            } else {
                console.error('Failed to load service types.')
            }
        } catch (error) {
            console.error('Error fetching service types:', error);
        }
    }
    loadServiceTypes();
    // Event listener for adding a new service type
    addButton.addEventListener('click', async function () {
        const name = nameInput.value.trim();
        const description = descriptionInput.value.trim();
        // Validate inputs
        if (!name || !description) {
            showToast('Please fill out both the name and desctiption fields.', 'danger');
            return;
        }
        data = {
            name: name,
            description: description
        }
        try {
            // send POST request
            const response = await fetch('http://localhost:8000/api/service/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                nameInput.value = '';
                descriptionInput.value = '';
                loadServiceTypes();
                showToast('Service type added successfully!', 'success');
            } else {
                const errorData = await response.json();
                showToast(`Error: ${errorData.detail || 'Failed to add service type.'}`, 'danger');
            }
        } catch (error) {
            showToast('An error occurred while adding the service type.', 'danger');
        }
    });
    // Function to display a toast notification
    function showToast(message, type) {
        const toastElement = document.getElementById('toast');
        const toast = bootstrap.Toast(toastElement);
        const toastBodyElement = document.getElementById('toastBody');
        toastElement.className = `toast align-items-center text-white bg-primary border-0 bg-${type}`;
        toastBodyElement.innerText = '';
        toastBodyElement.innerText = message;
        toast.show();
    }
});
