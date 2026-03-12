const express = require("express");

const app = express();

function paginaHTML(titulo, color, descripcion) {
    return `
    <html>
    <head>
        <title>${titulo}</title>
        <style>
            body{
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            .card{
                background:white;
                padding:40px;
                border-radius:10px;
                box-shadow:0 4px 15px rgba(0,0,0,0.15);
                text-align:center;
                width:400px;
            }

            h1{
                color:${color};
            }

            .estado{
                margin-top:20px;
                padding:10px;
                border-radius:6px;
                background:${color};
                color:white;
                font-weight:bold;
            }

            .info{
                margin-top:15px;
                color:#555;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <h1>${titulo}</h1>

            <div class="estado">
                Servicio activo
            </div>

            <p class="info">${descripcion}</p>

        </div>

    </body>
    </html>
    `;
}

app.get("/usuarios", (req, res) => {

    res.send(
        paginaHTML(
            "Servicio de Usuarios",
            "#2E86DE",
            "Este servicio gestiona la información de los usuarios del sistema."
        )
    );

});

app.get("/pedidos", (req, res) => {

    res.send(
        paginaHTML(
            "Servicio de Pedidos",
            "#E67E22",
            "Este servicio administra la creación y gestión de pedidos."
        )
    );

});

const PORT = 3000;

app.listen(PORT, () => {
    console.log("Servidor corriendo en puerto " + PORT);
});