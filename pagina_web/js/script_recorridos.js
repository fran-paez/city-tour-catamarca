const checks_dias = document.querySelectorAll('.dias');
const check_diario = document.getElementById("check_diario");

// ante un cambio de check diario, hace lo mismo con los checks de todos los dias
check_diario.addEventListener('change', function() {
    checks_dias.forEach(element => {
        element.checked = check_diario.checked;
    });
});

// Añadir un escuchador de eventos a cada checkbox
checks_dias.forEach(checkbox => {
    checkbox.addEventListener('change', actualizarCheckDiario);
    checkbox.addEventListener('change', ocultarAlert);
});
check_diario.addEventListener('change', ocultarAlert);

// Función para manejar el evento, actualizar el estado del checkbox 'diariamente'
function actualizarCheckDiario() {
    const totalOpciones = checks_dias.length;
    const opcionesMarcadas = document.querySelectorAll('.dias:checked').length;

    // si todos se marcaron
    if (opcionesMarcadas == totalOpciones) {
        check_diario.checked = true; //marcar el diario
    } else {
        check_diario.checked = false; // si no, desmarcar
    }
}

// ocultar la alerta de advertencia de dias necesarios
function ocultarAlert() {
    const dias_alert = document.getElementById("dias_alert");
    dias_alert.style.visibility = "hidden";
}

// Al apretar submit verifica primero que al menos se haya marcado un dia para el recorrido
document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault();
    const dias_alert = document.getElementById("dias_alert");

    const opcionesMarcadas = document.querySelectorAll('.dias:checked').length;
        
    if (opcionesMarcadas == 0) {
        dias_alert.style.visibility = "visible";
    } else {
        dias_alert.style.visibility = "hidden";
    }
});

