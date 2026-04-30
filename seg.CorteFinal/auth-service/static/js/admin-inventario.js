let lista = [];
const API_BASE = "http://localhost:5000/api";
let productoEditandoId = null;
let modalProductoInst = null;

function abrirModalProducto(){
  if(!modalProductoInst){
    modalProductoInst = new bootstrap.Modal(document.getElementById('modalProducto'));
  }
  modalProductoInst.show();
}

function limpiarFormulario(){
  productoEditandoId = null;
  const modalTitulo = document.getElementById("modalTitulo");
  if(modalTitulo) modalTitulo.innerText = "Nuevo Producto";

  const nombre = document.getElementById("nombre");
  const precio = document.getElementById("precio");
  const tipo = document.getElementById("tipo");
  const stock = document.getElementById("stock");
  const imagen = document.getElementById("imagen");
  const msgForm = document.getElementById("msgForm");

  if(nombre) nombre.value = "";
  if(precio) precio.value = "";
  if(tipo) tipo.value = "pizza";
  if(stock) stock.value = "";
  if(imagen) imagen.value = "";
  if(msgForm){
    msgForm.className = "small mt-2";
    msgForm.innerHTML = "";
  }
}

function render(data){
  const productos = document.getElementById("productos");
  if(!productos) return;

  let html = "";
  data.forEach(p => {
    html += `
      <div class="col-md-3">
        <div class="card mb-3 shadow-sm">
          <img src="${p[5] || 'https://via.placeholder.com/200'}" class="card-img-top producto-img">
          <div class="card-body text-center">
            <h6>${p[1]}</h6>
            <p class="mb-1">$${p[3]}</p>
            <small class="text-muted">Stock: ${p[4] ?? "N/A"}</small>
            <div class="mt-2">
              <button onclick="editar(${p[0]})" class="btn btn-warning btn-sm">Editar</button>
              <button onclick="estado(${p[0]})" class="btn btn-danger btn-sm">Eliminar</button>
            </div>
          </div>
        </div>
      </div>
    `;
  });
  productos.innerHTML = html;
}

window.filtrar = function filtrar(tipo){
  if(tipo === "todos") return render(lista);
  render(lista.filter(p => p[2] === tipo));
};

window.guardar = function guardar(){
  const msgForm = document.getElementById("msgForm");
  const nombre = document.getElementById("nombre");
  const precio = document.getElementById("precio");
  const tipo = document.getElementById("tipo");
  const stock = document.getElementById("stock");
  const imagen = document.getElementById("imagen");

  if(msgForm){
    msgForm.className = "small mt-2";
    msgForm.innerHTML = "";
  }

  if(!nombre?.value || !precio?.value){
    if(msgForm){
      msgForm.className = "small mt-2 text-danger";
      msgForm.innerText = "Campos obligatorios: nombre y precio.";
    }
    return;
  }

  const payload = {
    nombre: nombre.value,
    tipo: tipo?.value,
    precio: Number(precio.value),
    stock: stock?.value === "" ? null : Number(stock.value),
    imagen: imagen?.value
  };

  const url = productoEditandoId ? `${API_BASE}/productos/${productoEditandoId}` : `${API_BASE}/productos`;
  const method = productoEditandoId ? "PUT" : "POST";

  fetch(url, {
    method,
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  })
  .then(async (res) => {
    const data = await res.json().catch(() => ({}));
    if(!res.ok) return Promise.reject(data);
    return data;
  })
  .then((data) => {
    if(data?.error){
      if(msgForm){
        msgForm.className = "small mt-2 text-danger";
        msgForm.innerText = data.error;
      }
      return;
    }

    if(msgForm){
      msgForm.className = "small mt-2 text-success";
      msgForm.innerText = productoEditandoId ? "Producto actualizado correctamente." : "Producto agregado correctamente.";
    }
    setTimeout(() => location.reload(), 700);
  })
  .catch((err) => {
    if(msgForm){
      msgForm.className = "small mt-2 text-danger";
      msgForm.innerText = err?.error || "No se pudo guardar el producto.";
    }
  });
};

window.editar = function editar(id){
  const p = lista.find(x => x[0] === id);
  if(!p){
    alert("Producto no encontrado.");
    return;
  }

  productoEditandoId = id;
  const modalTitulo = document.getElementById("modalTitulo");
  if(modalTitulo) modalTitulo.innerText = `Editar Producto #${id}`;

  const nombre = document.getElementById("nombre");
  const precio = document.getElementById("precio");
  const tipo = document.getElementById("tipo");
  const stock = document.getElementById("stock");
  const imagen = document.getElementById("imagen");
  const msgForm = document.getElementById("msgForm");

  if(nombre) nombre.value = p[1] ?? "";
  if(tipo) tipo.value = p[2] ?? "pizza";
  if(precio) precio.value = p[3] ?? "";
  if(stock) stock.value = (p[4] == null) ? "" : p[4];
  if(imagen) imagen.value = p[5] ?? "";

  if(msgForm){
    msgForm.className = "small mt-2";
    msgForm.innerHTML = "";
  }

  abrirModalProducto();
};

window.estado = function estado(id){
  fetch(`${API_BASE}/productos/${id}/estado`,{
    method:"PUT",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({activo:false})
  }).then(()=>location.reload());
};

// init
document.addEventListener("DOMContentLoaded", () => {
  fetch(`${API_BASE}/productos`)
    .then(res => res.json())
    .then(data => {
      lista = data;
      render(lista);
    });

  // Reset cuando se abre como "Nuevo Producto"
  document.querySelector('[data-bs-target="#modalProducto"]')?.addEventListener("click", () => {
    limpiarFormulario();
  });

  // Limpieza al cerrar (por cancelar o X)
  document.getElementById("modalProducto")?.addEventListener("hidden.bs.modal", () => {
    limpiarFormulario();
  });
});

