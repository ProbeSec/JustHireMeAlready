async function cargarCandidaturas() {
    const respuesta = await fetch("http://127.0.0.1:8000/candidaturas");
    const datos = await respuesta.json();
    console.log(datos);

    // Agarramos la tabla
    const tbody = document.getElementById("lista-candidaturas");
    tbody.innerHTML = "";   // Vacía la tabla antes de rellenar (evita duplicados al recargar)

    // Recorremos las candidaturas
    datos.forEach(function(candidatura) {
        // Por CADA candidatura, metemos una fila
        tbody.innerHTML += `
            <tr>
                <td>${candidatura[3]}</td>   <!-- empresa -->
                <td>${candidatura[4]}</td>   <!-- puesto -->
                <td>${candidatura[1]}</td>   <!-- estado -->
                <td>${candidatura[2]}</td>   <!-- fecha -->
                <td>${candidatura[7]}</td>   <!-- ubicacion -->
                <td>${candidatura[8]}</td>   <!-- modalidad -->
                <td>${candidatura[6]}</td>   <!-- portal -->
                <td><a href="${candidatura[5]}" target="_blank">Ver</a></td>   <!-- link_oferta -->
                <td>
                    <button onclick="borrarCandidatura('${candidatura[0]}')">Borrar</button>
                    <button onclick="cambiarEstado('${candidatura[0]}')">Estado</button>
                    <button onclick="editarCandidatura('${candidatura[0]}')">Editar</button>
                </td>
            </tr>
        `;
    });
}

async function borrarCandidatura(id) {
    await fetch("http://127.0.0.1:8000/candidaturas/" + id, {
        method: "DELETE"
    });
    cargarCandidaturas();
}

async function anadirCandidatura() {
    const nueva = {
        estado: document.getElementById("estado").value,
        fecha_peticion: document.getElementById("fecha_peticion").value,
        empresa: document.getElementById("empresa").value,
        puesto: document.getElementById("puesto").value,
        link_oferta: document.getElementById("link_oferta").value,
        portal: document.getElementById("portal").value,
        ubicacion: document.getElementById("ubicacion").value,
        modalidad: document.getElementById("modalidad").value
    };

    await fetch("http://127.0.0.1:8000/candidaturas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nueva)
    });

    cargarCandidaturas();
}

async function cambiarEstado(id) {
    const nuevoEstado = prompt("Nuevo estado (enviada/contactado/entrevista/oferta/rechazada/pendiente):");

    if (nuevoEstado === null) {
        return;   // Si cancela, no hacemos nada
    }

    await fetch("http://127.0.0.1:8000/candidaturas/" + id, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado: nuevoEstado })
    });

    cargarCandidaturas();
}

async function editarCandidatura(id) {
    const estado = prompt("Estado (enviada/contactado/entrevista/oferta/rechazada/pendiente):");
    const fecha_peticion = prompt("Fecha (AAAA-MM-DD):");
    const empresa = prompt("Empresa:");
    const puesto = prompt("Puesto:");
    const link_oferta = prompt("Link:");
    const portal = prompt("Portal:");
    const ubicacion = prompt("Ubicación:");
    const modalidad = prompt("Modalidad:");

    await fetch("http://127.0.0.1:8000/candidaturas/" + id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad })
    });

    cargarCandidaturas();
}

document.getElementById("btn-anadir").onclick = anadirCandidatura;

cargarCandidaturas();