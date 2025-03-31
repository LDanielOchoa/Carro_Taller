document.addEventListener('DOMContentLoaded', function () {
    // Obtener todos los contenedores de select personalizados
    const customSelectContainers = document.querySelectorAll('.custom-select-container');

    // Iterar por cada contenedor
    customSelectContainers.forEach((container) => {
        const customSelect = container.querySelector('.custom-select');
        const dropdown = container.querySelector('.dropdown');
        const options = dropdown.querySelectorAll('.option');

        // Mostrar/Ocultar el dropdown al hacer clic en el select
        customSelect.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevenir propagación para evitar conflictos con el evento global
            const isOpen = container.classList.contains('open');
            closeAllDropdowns(); // Cierra todos los desplegables abiertos
            if (!isOpen) {
                container.classList.add('open');
            }
        });

        // Seleccionar una opción y cerrar el dropdown
        options.forEach((option) => {
            option.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevenir cierre inmediato por el evento global
                customSelect.textContent = option.textContent; // Actualiza el texto del select
                customSelect.dataset.value = option.dataset.value; // Guarda el valor
                container.classList.remove('open'); // Cierra el menú
            });
        });
    });

    // Cerrar todos los dropdowns al hacer clic fuera de ellos
    document.addEventListener('click', () => {
        closeAllDropdowns();
    });

    // Función para cerrar todos los dropdowns abiertos
    function closeAllDropdowns() {
        document.querySelectorAll('.custom-select-container.open').forEach((container) => {
            container.classList.remove('open');
        });
    }
});

flatpickr(".timepicker", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",  // Formato de la hora
    time_24hr: true,
    minuteIncrement: 10,  // Intervalos de 10 minutos
    onChange: function (selectedDates, dateStr, instance) {
        console.log(dateStr);  // Muestra la hora seleccionada
    }
});


