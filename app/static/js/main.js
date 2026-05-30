// Favorites toggle via AJAX
function toggleFavorite(ofertaId, button) {
    fetch(`/user/favoritos/toggle/${ofertaId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrf_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.action === 'added') {
                button.textContent = '❤️';
                button.classList.add('favorited');
            } else {
                button.textContent = '🤍';
                button.classList.remove('favorited');
            }
            showToast(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Get CSRF token from cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Show toast notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'alert alert-success';
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '1000';
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Initialize Leaflet map
function initMap(elementId, lat, lng) {
    const map = L.map(elementId).setView([lat, lng], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    L.marker([lat, lng]).addTo(map);
    
    return map;
}

// Image gallery
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const modal = document.getElementById('gallery-modal');
    
    if (!modal) return;
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imgSrc = this.src;
            document.getElementById('modal-image').src = imgSrc;
            modal.style.display = 'flex';
        });
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.classList.contains('close')) {
            modal.style.display = 'none';
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initGallery();
});
