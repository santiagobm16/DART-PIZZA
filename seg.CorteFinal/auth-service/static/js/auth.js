const AUTH_BASE = "";

function byId(id) {
    return document.getElementById(id);
}

function showMessage(text, type = "danger") {
    const box = byId("form-msg");
    if (!box) return;
    box.className = `alert alert-${type} mt-3 mb-0`;
    box.textContent = text;
    box.classList.remove("d-none");
}

function clearMessage() {
    const box = byId("form-msg");
    if (!box) return;
    box.classList.add("d-none");
    box.textContent = "";
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function login() {
    clearMessage();
    const email = byId("email")?.value?.trim();
    const password = byId("password")?.value ?? "";

    if (!email || !password) {
        showMessage("Completa correo y contraseña.");
        return;
    }

    if (!isValidEmail(email)) {
        showMessage("Ingresa un correo valido.");
        return;
    }

    fetch(`${AUTH_BASE}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email,
            password
        })
    })
    .then(async res => ({ok: res.ok, data: await res.json()}))
    .then(data => {
        if (!data.ok) {
            showMessage(data.data.error || "No se pudo iniciar sesión.");
            return;
        }
        if (data.data.rol === "admin") window.location = "/admin";
        else window.location = "/cliente";
    })
    .catch(() => showMessage("Error de conexión con el servidor."));
}

function registro() {
    clearMessage();
    const nombre = byId("nombre")?.value?.trim();
    const email = byId("email")?.value?.trim();
    const password = byId("password")?.value ?? "";
    const confirmPassword = byId("confirm")?.value ?? "";

    if (!nombre || !email || !password || !confirmPassword) {
        showMessage("Todos los campos son obligatorios.");
        return;
    }

    if (!isValidEmail(email)) {
        showMessage("Ingresa un correo valido.");
        return;
    }

    if (password !== confirmPassword) {
        showMessage("Las contraseñas no coinciden.");
        return;
    }

    fetch(`${AUTH_BASE}/registro`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nombre,
            email,
            password,
            rol1: "cliente"
        })
    })
    .then(async res => ({ok: res.ok, data: await res.json()}))
    .then(result => {
        if (!result.ok) {
            showMessage(result.data.error || "No se pudo crear la cuenta.");
            return;
        }
        showMessage("Cuenta creada. Redirigiendo...", "success");
        setTimeout(() => window.location = "/", 700);
    })
    .catch(() => showMessage("Error de conexión con el servidor."));
}