/**
 * Admin Offer Form - Dynamic Field Management
 * Shows/hides sections based on tipo_operacion and tipo_propiedad selections
 */

function initOfferForm() {
    console.log('Initializing Offer Form dynamic logic...');

    // Basic fields
    const tipoOperacion = document.querySelector('[name="tipo_operacion"]');
    const tipoPropiedad = document.querySelector('[name="tipo_propiedad"]');
    const ubicacion = document.querySelector('[name="ubicacion"]');
    const barrio = document.querySelector('[name="barrio"]');

    // Dynamic sections
    const sectionTipoAlquiler = document.getElementById('section-tipo-alquiler');
    const sectionsProperty = {
        'vivienda': document.getElementById('additional-vivienda'),
        'oficinas': document.getElementById('additional-oficina'),
        'locales_naves': document.getElementById('additional-locales_naves'),
        'terrenos': document.getElementById('additional-terrenos')
    };

    // Location coordinates for EG cities
    const cityCoordinates = {
        'Malabo': [3.7504, 8.7715],
        'Bata': [1.8636, 9.7658],
        'Luba': [3.4568, 8.5547],
        'Ebebiyín': [2.1511, 11.3353],
        'Mongomo': [1.6274, 11.3124],
        'Evinayong': [1.4461, 10.5519],
        'Oyala': [1.5833, 10.8333], // Ciudad de la Paz
        'Annobon': [-1.4326, 5.6318],
        'Riaba': [3.3775, 8.7619],
        'Baney': [3.7083, 8.8786],
        'Rebola': [3.7167, 8.8],
        'Mbini': [1.5826, 9.6134],
        'Cogo': [1.0841, 9.6934],
        'Niefang': [2.0116, 10.2525],
        'Anisoc': [1.8647, 10.7675],
        'Micomeseng': [2.14, 10.61],
        'Nsork': [1.13, 11.25]
    };

    // Map initialization
    const mapContainer = document.getElementById('map');
    const latField = document.getElementById('lat-field');
    const lngField = document.getElementById('lng-field');
    const coordPreview = document.getElementById('coordinates-preview');

    let map, marker;

    if (mapContainer && typeof L !== 'undefined') {
        const initialLat = parseFloat(latField?.value) || 3.7504;
        const initialLng = parseFloat(lngField?.value) || 8.7715;

        // Limpiar instancia previa si existe (importante para modales)
        if (mapContainer._leaflet_id) {
            mapContainer._leaflet_id = null;
        }

        map = L.map('map').setView([initialLat, initialLng], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        marker = L.marker([initialLat, initialLng], {
            draggable: true
        }).addTo(map);

        marker.on('dragend', function (event) {
            const position = marker.getLatLng();
            updateCoordinates(position.lat, position.lng);
        });

        map.on('click', function (e) {
            marker.setLatLng(e.latlng);
            updateCoordinates(e.latlng.lat, e.latlng.lng);
        });
    }

    function updateCoordinates(lat, lng) {
        if (latField) latField.value = lat.toFixed(6);
        if (lngField) lngField.value = lng.toFixed(6);
        if (coordPreview) {
            coordPreview.textContent = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
        }
    }

    function updateFormVisibility() {
        const operacion = tipoOperacion?.value || '';
        const propiedad = tipoPropiedad?.value || '';

        // 1. Tipo de alquiler (Solo para alquiler o compartir)
        if (sectionTipoAlquiler) {
            sectionTipoAlquiler.style.display = (operacion === 'alquiler' || operacion === 'compartir') ? 'block' : 'none';
        }

        // 2. Clear all property sections first
        Object.values(sectionsProperty).forEach(sec => {
            if (sec) sec.style.display = 'none';
        });

        // 3. Show specific property section
        if (propiedad && sectionsProperty[propiedad]) {
            sectionsProperty[propiedad].style.display = 'block';
        }
    }

    function onCityChange() {
        const cityName = ubicacion?.value;
        if (cityName && cityCoordinates[cityName] && map) {
            const coords = cityCoordinates[cityName];
            map.setView(coords, 13);
            marker.setLatLng(coords);
            updateCoordinates(coords[0], coords[1]);
        }
    }

    // Event listeners
    if (tipoOperacion) tipoOperacion.addEventListener('change', updateFormVisibility);
    if (tipoPropiedad) tipoPropiedad.addEventListener('change', updateFormVisibility);
    if (ubicacion) ubicacion.addEventListener('change', onCityChange);

    // Initial run
    updateFormVisibility();

    // Trigger map resize fix if in modal
    setTimeout(() => {
        if (map) map.invalidateSize();
    }, 500);

    // Date validation
    const fechaBaja = document.querySelector('[name="fecha_baja_programada"]');
    if (fechaBaja) {
        fechaBaja.addEventListener('change', function () {
            if (!this.value) return;
            const selectedDate = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (selectedDate < today) {
                alert('La fecha de baja programada no puede ser anterior a hoy.');
                this.value = '';
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', initOfferForm);
window.initOfferForm = initOfferForm;

document.addEventListener('DOMContentLoaded', initOfferForm);
window.initOfferForm = initOfferForm;
