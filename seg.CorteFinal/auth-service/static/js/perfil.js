function getEl(id){
  return document.getElementById(id);
}

function mostrarMensaje(texto, tipo = "success"){
  const perfilMsg = getEl("perfilMsg");
  if(!perfilMsg) return;

  perfilMsg.className = `alert alert-${tipo} mt-3 mb-0`;
  perfilMsg.textContent = texto;
  perfilMsg.classList.remove("d-none");
}

function correoValido(correo){
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(correo || ""));
}

window.actualizar = function actualizar(){
  const nuevoNombre = getEl("nuevoNombre");
  const nuevoEmail = getEl("nuevoEmail");
  if(!nuevoNombre || !nuevoEmail) return;

  const nombre = nuevoNombre.value.trim();
  const email = nuevoEmail.value.trim();

  if(!nombre || !email){
    mostrarMensaje("Nombre y correo son obligatorios.", "danger");
    return;
  }

  if(!correoValido(email)){
    mostrarMensaje("Ingresa un correo valido.", "danger");
    return;
  }

  fetch("/perfil", {
    method: "PUT",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({nombre, email})
  })
  .then(async (res) => ({ ok: res.ok, data: await res.json().catch(() => ({})) }))
  .then(result => {
    if(!result.ok){
      mostrarMensaje(result.data?.error || "No se pudo actualizar el perfil.", "danger");
      return;
    }
    const modalEl = getEl("modalEditarPerfil");
    if(modalEl){
      bootstrap.Modal.getInstance(modalEl)?.hide();
    }
    mostrarMensaje("Perfil actualizado correctamente.");
    setTimeout(() => location.reload(), 700);
  });
};

window.cambiarPass = function cambiarPass(){
  const pass1 = getEl("pass1");
  const pass2 = getEl("pass2");
  if(!pass1 || !pass2) return;

  if(pass1.value !== pass2.value){
    mostrarMensaje("Las contraseñas no coinciden.", "danger");
    return;
  }

  if(!pass1.value.trim()){
    mostrarMensaje("La contraseña no puede estar vacia.", "danger");
    return;
  }

  fetch("/cambiar-password", {
    method: "PUT",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ password: pass1.value })
  })
  .then(async (res) => ({ ok: res.ok, data: await res.json().catch(() => ({})) }))
  .then(result => {
    if(!result.ok){
      mostrarMensaje(result.data?.error || "No se pudo actualizar la contraseña.", "danger");
      return;
    }
    const modalEl = getEl("modalPassword");
    if(modalEl){
      bootstrap.Modal.getInstance(modalEl)?.hide();
    }
    mostrarMensaje("Contraseña actualizada correctamente.");
    pass1.value = "";
    pass2.value = "";
  });
};

