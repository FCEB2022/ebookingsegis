/**
 * Search Filters Dynamic Behavior
 * Handles showing/hiding dependent filter fields based on property type selection
 */

document.addEventListener('DOMContentLoaded', function () {
    const tipoPropiedad = document.getElementById('tipo_propiedad');
    const tipologiaLocal = document.getElementById('tipologia_local');

    // Filter field containers
    const filtrosVivienda = document.getElementById('filtros_vivienda');
    const filtrosLocales = document.getElementById('filtros_locales');
    const filtrosOficinas = document.getElementById('filtros_oficinas');
    const filtrosTerrenos = document.getElementById('filtros_terrenos');
    const caracteristicasLocalContainer = document.getElementById('caracteristicas_local_container');

    // Initialize on page load
    if (tipoPropiedad) {
        toggleFilterSections();
        tipoPropiedad.addEventListener('change', toggleFilterSections);
    }

    // Handle local caracteristicas visibility based on tipologia
    if (tipologiaLocal) {
        toggleLocalCaracteristicas();
        tipologiaLocal.addEventListener('change', toggleLocalCaracteristicas);
    }

    /**
     * Show/hide filter sections based on selected property type
     */
    function toggleFilterSections() {
        const selectedType = tipoPropiedad.value;

        // Hide all dependent filters first
        if (filtrosVivienda) filtrosVivienda.style.display = 'none';
        if (filtrosLocales) filtrosLocales.style.display = 'none';
        if (filtrosOficinas) filtrosOficinas.style.display = 'none';
        if (filtrosTerrenos) filtrosTerrenos.style.display = 'none';

        // Show relevant section
        switch (selectedType) {
            case 'vivienda':
                if (filtrosVivienda) filtrosVivienda.style.display = 'block';
                break;
            case 'locales_naves':
                if (filtrosLocales) filtrosLocales.style.display = 'block';
                toggleLocalCaracteristicas();
                break;
            case 'oficinas':
                if (filtrosOficinas) filtrosOficinas.style.display = 'block';
                break;
            case 'terrenos':
                if (filtrosTerrenos) filtrosTerrenos.style.display = 'block';
                break;
            default:
                // 'Indiferente' - all hidden
                break;
        }
    }

    /**
     * Show caracteristicas only for comercial, ocio, eventos
     */
    function toggleLocalCaracteristicas() {
        if (!caracteristicasLocalContainer) return;

        const tipologia = tipologiaLocal.value;
        const showCaracteristicas = ['comercial', 'ocio', 'eventos'].includes(tipologia);

        caracteristicasLocalContainer.style.display = showCaracteristicas ? 'block' : 'none';
    }

    /**
     * Handle form submission - build query string from filters
     */
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            // Remove empty fields to keep URL clean
            const inputs = searchForm.querySelectorAll('input, select');
            inputs.forEach(input => {
                if (!input.value || input.value === '') {
                    input.disabled = true;
                }
            });
        });
    }

    /**
     * Clear all filters
     */
    const clearBtn = document.getElementById('clear-filters');
    if (clearBtn) {
        clearBtn.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = window.location.pathname; // Reload without query params
        });
    }

    /**
     * Toggle filter panel on mobile
     */
    const filterToggleBtn = document.getElementById('toggle-filters');
    const filterPanel = document.getElementById('filter-panel');

    if (filterToggleBtn && filterPanel) {
        filterToggleBtn.addEventListener('click', function () {
            filterPanel.classList.toggle('show');
            this.textContent = filterPanel.classList.contains('show') ? 'Ocultar filtros' : 'Mostrar filtros';
        });
    }
});
