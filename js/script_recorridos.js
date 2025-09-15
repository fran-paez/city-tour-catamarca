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
});

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