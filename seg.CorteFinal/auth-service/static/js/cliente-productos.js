let lista = [];
let carrito = [];
const API_BASE = "http://localhost:5000/api";
const sessionEl = document.getElementById("sessionData");
const USER_ID = sessionEl ? Number(sessionEl.dataset.userId || 0) : 0;

fetch(`${API_BASE}/productos`)
.then(res => res.json())
.then(data => {
    lista = data;
    render(data);
});

function render(data){
    let html = "";

    data.forEach(p => {
        html += `
        <div class="col-md-3">
          <div class="card mb-3 shadow-sm">

            <img src="${p[5] || 'https://via.placeholder.com/200'}" class="card-img-top producto-img">

            <div class="card-body text-center">
              <h6>${p[1]}</h6>
              <p>$${p[3]}</p>

              <div class="d-flex justify-content-center align-items-center">
                <button onclick="restar(${p[0]})" class="btn btn-outline-dark btn-sm">-</button>
                <span id="c${p[0]}" class="mx-2">0</span>
                <button onclick="sumar(${p[0]})" class="btn btn-outline-dark btn-sm">+</button>
              </div>
            </div>

          </div>
        </div>`;
    });

    productos.innerHTML = html;
}

function filtrar(tipo){
    if(tipo === "todos") return render(lista);
    render(lista.filter(p => p[2] === tipo));
}

function sumar(id){
    let item = carrito.find(p => p.producto_id === id);

    if(item) item.cantidad++;
    else carrito.push({producto_id:id, cantidad:1});

    actualizarUI();
}

function restar(id){
    let item = carrito.find(p => p.producto_id === id);
    if(!item) return;

    item.cantidad--;
    if(item.cantidad <= 0){
        carrito = carrito.filter(p => p.producto_id !== id);
    }

    actualizarUI();
}

function actualizarUI(){
    let total = 0;

    lista.forEach(p => {
        let item = carrito.find(c => c.producto_id === p[0]);
        let cantidad = item ? item.cantidad : 0;

        document.getElementById(`c${p[0]}`).innerText = cantidad;

        if(item) total += p[3] * item.cantidad;
    });

    totalTxt.innerText = `Total: $${total}`;
}

document.getElementById("modalPedido").addEventListener("show.bs.modal", ()=>{
    if(carrito.length === 0){
        alert("No has seleccionado productos");
        event.preventDefault();
        return;
    }

    let html = "";
    let total = 0;

    carrito.forEach(c => {
        let p = lista.find(x => x[0] === c.producto_id);
        const precio = Number(p[3]) || 0;
        const subtotal = precio * c.cantidad;
        total += subtotal;

        html += `
          <div class="d-flex justify-content-between">
            <span>${p[1]} x${c.cantidad}</span>
            <span>$${precio.toLocaleString()} (Sub: $${subtotal.toLocaleString()})</span>
          </div>
        `;
    });

    html += `<hr><div class="d-flex justify-content-between"><b>Total</b><b>$${total.toLocaleString()}</b></div>`;
    resumen.innerHTML = html;
});

// mostrar dirección solo si es domicilio
tipo.addEventListener("change", ()=>{
    direccion.style.display = tipo.value === "domicilio" ? "block" : "none";
});

function confirmarPedido(){

    if(!USER_ID){
        alert("Sesión no válida. Vuelve a iniciar sesión.");
        window.location = "/";
        return;
    }

    if(tipo.value === "domicilio" && !direccion.value){
        alert("Debes ingresar la dirección");
        return;
    }

    fetch(`${API_BASE}/pedidos`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
            usuario_id: USER_ID,
            tipo: tipo.value,
            direccion: direccion.value,
            productos: carrito
        })
    })
    .then(async (res) => {
        const data = await res.json().catch(() => ({}));
        if(!res.ok){
            throw new Error(data?.error || "No se pudo crear el pedido");
        }
        return data;
    })
    .then(() => {
        alert("Tu pedido fue realizado correctamente.");
        carrito = [];
        location.reload();
    })
    .catch(err => alert(err.message || "Error realizando el pedido"));
}

