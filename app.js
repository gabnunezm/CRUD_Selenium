let vehicles = JSON.parse(localStorage.getItem('vehicles')) || [];
let editingId = null;

// Elementos del DOM
const form = document.getElementById('vehicle-form');
const vehicleList = document.getElementById('vehicle-list');
const saveBtn = document.getElementById('save-btn');
const clearBtn = document.getElementById('clear-btn');

// Guardar vehículo
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const vehicle = {
        id: editingId || Date.now().toString(),
        brand: document.getElementById('brand').value,
        model: document.getElementById('model').value,
        year: document.getElementById('year').value,
        price: document.getElementById('price').value,
        color: document.getElementById('color').value
    };

    if (editingId) {
        const index = vehicles.findIndex(v => v.id === editingId);
        vehicles[index] = vehicle;
    } else {
        vehicles.push(vehicle);
    }

    localStorage.setItem('vehicles', JSON.stringify(vehicles));
    resetForm();
    renderVehicles();
});

// Mostrar vehículos
function renderVehicles() {
    vehicleList.innerHTML = vehicles.map(vehicle => `
        <tr class="border text-center">
            <td class="p-2 border">${vehicle.brand}</td>
            <td class="p-2 border">${vehicle.model}</td>
            <td class="p-2 border">${vehicle.year}</td>
            <td class="p-2 border">$${vehicle.price}</td>
            <td class="p-2 border">${vehicle.color}</td>
            <td class="p-2 border">
                <button onclick="editVehicle('${vehicle.id}')" class="bg-yellow-500 text-white px-2 py-1 rounded mr-2">
                    Editar
                </button>
                <button onclick="deleteVehicle('${vehicle.id}')" class="bg-red-500 text-white px-2 py-1 rounded">
                    Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

// Editar vehículo
function editVehicle(id) {
    const vehicle = vehicles.find(v => v.id === id);
    if (!vehicle) return;

    editingId = id;
    document.getElementById('brand').value = vehicle.brand;
    document.getElementById('model').value = vehicle.model;
    document.getElementById('year').value = vehicle.year;
    document.getElementById('price').value = vehicle.price;
    document.getElementById('color').value = vehicle.color;
    
    saveBtn.textContent = 'Actualizar';
    saveBtn.classList.remove('bg-blue-600');
    saveBtn.classList.add('bg-green-600');
}

// Eliminar vehículo
function deleteVehicle(id) {
    vehicles = vehicles.filter(v => v.id !== id);
    localStorage.setItem('vehicles', JSON.stringify(vehicles));
    renderVehicles();
}

// Limpiar formulario
function resetForm() {
    form.reset();
    editingId = null;
    saveBtn.textContent = 'Guardar';
    saveBtn.classList.remove('bg-green-600');
    saveBtn.classList.add('bg-blue-600');
}

// Event listener para limpiar
clearBtn.addEventListener('click', resetForm);

// Inicializar
renderVehicles();