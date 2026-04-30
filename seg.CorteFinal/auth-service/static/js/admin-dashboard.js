let pedidoSeleccionado = null;
const API_BASE = "http://localhost:5000/api";
let pedidosCache = [];

function badge(estado){
  switch(estado){
    case "pendiente": return '<span class="badge bg-secondary">Pendiente</span>';
    case "preparando": return '<span class="badge bg-warning text-dark">Preparando</span>';
    case "enviado": return '<span class="badge bg-primary">Enviado</span>';
    case "entregado": return '<span class="badge bg-success">Entregado</span>';
    case "rechazado": return '<span class="badge bg-danger">Rechazado</span>';
  }
}

async function cargar(){
  const data = await fetch(`${API_BASE}/pedidos`).then(r => r.json());
  pedidosCache = data;

  // precargar detalles
  const detalles = {};
  await Promise.all(
    data.map(async (p) => {
      const id = p[0];
      const res = await fetch(`${API_BASE}/pedidos/${id}/detalle`);
      if(res.ok) detalles[id] = await res.json();
      else detalles[id] = [];
    })
  );

  render(data, detalles);
}

function detalleHTML(items){
  if(!items || !items.length) return "<small class='text-muted'>Sin detalle</small>";
  return `
    <ul class="mb-0 ps-3">
      ${items.map(x => `<li><small>${x[0]} x${x[1]}</small></li>`).join("")}
    </ul>
  `;
}

function render(data, detalles){
  const buscador = document.getElementById("buscador");
  const tabla = document.getElementById("tabla");
  const pendientes = document.getElementById("pendientes");
  if(!buscador || !tabla || !pendientes) return;

  const q = (buscador.value || "").trim().toLowerCase();
  const match = (p) => {
    if(!q) return true;
    return String(p[0]).includes(q) ||
      String(p[4] || "").toLowerCase().includes(q) ||
      String(p[1]).toLowerCase().includes(q);
  };

  const filtrados = data.filter(match);

  const pendientesList = filtrados.filter(p => p[1] === "pendiente");
  const otrosList = filtrados.filter(p => p[1] !== "pendiente" && p[1] !== "rechazado");
  const rechazadosList = filtrados.filter(p => p[1] === "rechazado");

  // Cards pendientes
  pendientes.innerHTML = pendientesList.map(p => {
    const id = p[0];
    return `
      <div class="col-md-3">
        <div class="card p-3 shadow-sm">
          <h5>Pedido #${id}</h5>
          <p class="mb-1"><b>${p[4]}</b></p>
          <div class="mb-2">${detalleHTML(detalles[id])}</div>
          <p class="mb-2">$${p[3]}</p>

          <button class="btn btn-success btn-sm" onclick="estado(${id}, 'preparando')">Aceptar</button>
          <button class="btn btn-danger btn-sm mt-1" onclick="abrirModal(${id})">Rechazar</button>
        </div>
      </div>
    `;
  }).join("");

  // Tabla (otros + rechazados al final)
  const filas = [...otrosList, ...rechazadosList].map(p => {
    const id = p[0];
    let acciones = "";

    if(p[1] === "preparando"){
      acciones = `<button class="btn btn-warning btn-sm" onclick="estado(${id}, 'enviado')">Enviar</button>`;
    }
    if(p[1] === "enviado"){
      acciones = `<button class="btn btn-success btn-sm" onclick="estado(${id}, 'entregado')">Entregar</button>`;
    }
    if(p[1] === "rechazado"){
      acciones = `<small class="text-muted">${p[5] ? `Obs: ${p[5]}` : ""}</small>`;
    }

    return `
      <tr>
        <td>${id}</td>
        <td>${p[4]}</td>
        <td>${badge(p[1])}</td>
        <td>${detalleHTML(detalles[id])}</td>
        <td>$${p[3]}</td>
        <td>${acciones}</td>
      </tr>
    `;
  }).join("");

  tabla.innerHTML = filas;
}

window.estado = function estado(id, estado){
  fetch(`${API_BASE}/pedidos/${id}/estado`,{
    method:"PUT",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({estado})
  }).then(()=>location.reload());
};

window.abrirModal = function abrirModal(id){
  const tituloRechazo = document.getElementById("tituloRechazo");
  if(tituloRechazo){
    tituloRechazo.innerText = `Rechazar pedido #${id}`;
  }
  pedidoSeleccionado = id;
  new bootstrap.Modal(document.getElementById('modalRechazo')).show();
};

window.confirmarRechazo = function confirmarRechazo(){
  const observacion = document.getElementById("observacion");
  fetch(`${API_BASE}/pedidos/${pedidoSeleccionado}/rechazar`,{
    method:"PUT",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({observacion: observacion ? observacion.value : ""})
  }).then(()=>location.reload());
};

// init
document.addEventListener("DOMContentLoaded", () => {
  const buscador = document.getElementById("buscador");
  if(buscador){
    buscador.addEventListener("input", () => cargar());
  }
  cargar();
});

