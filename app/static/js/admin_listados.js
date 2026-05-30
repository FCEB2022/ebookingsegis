/**
 * SEGIS Admin - Listados y Acciones Masivas
 * Gestiona la selección de elementos en tablas y el envío de acciones en lote.
 */

document.addEventListener('DOMContentLoaded', function () {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.offer-checkbox');
    const selectedCountDisplay = document.getElementById('selected-count');
    const bulkButtons = document.querySelectorAll('.bulk-action');
    const bulkForm = document.getElementById('bulk-form');
    const bulkActionInput = document.getElementById('bulk-action-input');

    // Actualiza el contador de elementos seleccionados
    function updateCounter() {
        if (!checkboxes.length) return;
        const checked = document.querySelectorAll('.offer-checkbox:checked').length;
        if (selectedCountDisplay) {
            selectedCountDisplay.textContent = `${checked} seleccionadas`;
        }

        // Actualizar el estado del checkbox "seleccionar todos"
        if (selectAll) {
            selectAll.checked = (checked === checkboxes.length && checkboxes.length > 0);
            selectAll.indeterminate = (checked > 0 && checked < checkboxes.length);
        }
    }

    // Evento para seleccionar/deseleccionar todos
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            checkboxes.forEach(cb => {
                cb.checked = selectAll.checked;
                // Opcional: resaltar fila
                const row = cb.closest('tr');
                if (row) row.style.backgroundColor = selectAll.checked ? '#fff9c4' : '';
            });
            updateCounter();
        });
    }

    // Eventos para checkboxes individuales
    checkboxes.forEach(cb => {
        cb.addEventListener('change', function () {
            const row = cb.closest('tr');
            if (row) row.style.backgroundColor = cb.checked ? '#fff9c4' : '';
            updateCounter();
        });
    });

    // Eventos para botones de acción masiva
    bulkButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const action = this.getAttribute('data-action');
            const checkedCount = document.querySelectorAll('.offer-checkbox:checked').length;

            if (checkedCount === 0) {
                alert('Por favor, selecciona al menos una oferta.');
                return;
            }

            let confirmMsg = '';
            if (action === 'borrar') {
                confirmMsg = `⚠️ ¿Estás seguro de que deseas ELIMINAR permanentemente ${checkedCount} ofertas?\nEsta acción no se puede deshacer.`;
            } else if (action === 'activar') {
                confirmMsg = `¿Deseas marcar como ACTIVADAS ${checkedCount} ofertas? Serán visibles públicamente.`;
            } else if (action === 'desactivar') {
                confirmMsg = `¿Deseas DESACTIVAR ${checkedCount} ofertas? Dejarán de estar publicadas.`;
            }

            if (confirm(confirmMsg)) {
                if (bulkActionInput && bulkForm) {
                    bulkActionInput.value = action;
                    bulkForm.submit();
                }
            }
        });
    });

    // --- MODAL EDIT LOGIC ---
    const editModal = document.getElementById('edit-modal');
    const modalBody = document.getElementById('modal-body');
    const modalLoader = document.getElementById('modal-loader');

    // Open Modal
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.btn-edit-modal');
        if (btn) {
            const id = btn.getAttribute('data-id');
            showModal(id);
        }
    });

    function showModal(id) {
        if (!editModal) return;

        editModal.style.display = 'block';
        modalLoader.style.display = 'block';
        modalBody.innerHTML = '';
        document.body.style.overflow = 'hidden'; // Prevent scroll

        fetch(`/admin/ofertas/editar/${id}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.text())
            .then(html => {
                // Extract the form part if it's the whole page
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const mainContent = doc.querySelector('section.container');

                if (mainContent) {
                    modalBody.innerHTML = mainContent.innerHTML;
                    modalLoader.style.display = 'none';

                    // Re-init dynamic form logic
                    if (window.initOfferForm) {
                        window.initOfferForm();
                    }

                    // Handle form submission via AJAX if possible, or just let it redirect
                    // Let's add an interceptor for the modal form
                    const form = modalBody.querySelector('form');
                    if (form) {
                        // Update action to be full URL to avoid issues
                        form.action = `/admin/ofertas/editar/${id}`;
                    }
                } else {
                    modalBody.innerHTML = '<div style="padding: 20px; color: red;">Error: No se pudo cargar el contenido.</div>';
                    modalLoader.style.display = 'none';
                }
            })
            .catch(err => {
                console.error('Fetch error:', err);
                modalBody.innerHTML = '<div style="padding: 20px; color: red;">Error de red al cargar.</div>';
                modalLoader.style.display = 'none';
            });
    }

    // Close Modal
    if (editModal) {
        editModal.addEventListener('click', function (e) {
            if (e.target === editModal || e.target.closest('.btn-close')) {
                hideModal();
            }
        });

        // ESC key to close
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && editModal.style.display === 'block') {
                hideModal();
            }
        });
    }

    function hideModal() {
        editModal.style.display = 'none';
        document.body.style.overflow = '';
    }
});
