const API_BASE = "http://localhost:5000/api";
const sessionEl = document.getElementById("sessionData");
const USER_ID = sessionEl ? Number(sessionEl.dataset.userId || 0) : 0;

if(!USER_ID){
  alert("Sesión no válida. Vuelve a iniciar sesión.");
  window.location = "/";
}

fetch(`${API_BASE}/pedidos/usuario/${USER_ID}`)
  .then(res => res.json())
  .then(data => {
    const tabla = document.getElementById("tabla");
    if(!tabla) return;

    let html = "";
    let rechazadosConObs = [];

    data.forEach(p => {
      let color = "secondary";
      if(p[1] === "preparando") color = "warning";
      if(p[1] === "enviado") color = "primary";
      if(p[1] === "entregado") color = "success";
      if(p[1] === "rechazado") color = "danger";

      const obs = p[4] || "";
      if(p[1] === "rechazado" && obs) rechazadosConObs.push({id: p[0], obs});

      html += `
        <tr>
          <td>${p[0]}</td>
          <td><span class="badge bg-${color}">${p[1]}</span></td>
          <td>$${p[3]}</td>
          <td>${obs}</td>
        </tr>`;
    });

    tabla.innerHTML = html;

    // Alertar al cliente cuando haya rechazos nuevos (con observación)
    const lastSeen = Number(localStorage.getItem("lastSeenRejectedId") || 0);
    const nuevos = rechazadosConObs.filter(x => x.id > lastSeen);
    if(nuevos.length){
      const ultimo = Math.max(...rechazadosConObs.map(x => x.id));
      localStorage.setItem("lastSeenRejectedId", String(ultimo));
      alert(`Tu pedido fue rechazado:\n\n${nuevos.map(x => `Pedido #${x.id}: ${x.obs}`).join("\n")}`);
    }
  });

