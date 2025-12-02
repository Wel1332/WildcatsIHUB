// ============================================
// Professional Student Profile JavaScript
// ============================================

// This file should be loaded AFTER the HTML template has set window.profileDataFromDjango
// The actual profileData is now in the HTML file, passed from Django

// ============================================
// CSRF TOKEN FUNCTION
// ============================================

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================================
// SAVE DATA TO SUPABASE - CORRECTED FIELD NAMES
// ============================================

async function saveProfile(event) {
    event.preventDefault();
    
    try {
        // Get form values - USE CORRECT SUPABASE COLUMN NAMES
        const formData = new FormData();
        formData.append('full_name', document.getElementById('name').value);
        formData.append('title', document.getElementById('title').value);
        formData.append('school', document.getElementById('school').value);
        formData.append('year_level', document.getElementById('year').value);  // Correct
        formData.append('location', document.getElementById('location').value);
        formData.append('graduation_year', document.getElementById('graduation').value);  // CHANGED: graduation_year NOT graduation_yr
        formData.append('about', document.getElementById('about').value);
        formData.append('specialization', document.getElementById('specialization').value);
        formData.append('major', document.getElementById('major').value);
        formData.append('minor', document.getElementById('minor').value);
        formData.append('courses', document.getElementById('courses').value);
        formData.append('interests', document.getElementById('interests').value);
        
        // Send to Django backend
        const response = await fetch('/save-profile-to-supabase/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });

        const result = await response.json();
        
        if (result.success) {
            // Get the global profileData from HTML template
            if (window.profileDataFromDjango) {
                window.profileDataFromDjango = {
                    ...window.profileDataFromDjango,
                    name: document.getElementById('name').value,
                    title: document.getElementById('title').value,
                    school: document.getElementById('school').value,
                    year: document.getElementById('year').value,
                    location: document.getElementById('location').value,
                    about: document.getElementById('about').value,
                    graduation: document.getElementById('graduation').value,
                    specialization: document.getElementById('specialization').value,
                    major: document.getElementById('major').value,
                    minor: document.getElementById('minor').value,
                    courses: document.getElementById('courses').value,
                    interests: document.getElementById('interests').value
                };
                
                // Update the page display
                updateProfileDisplay(window.profileDataFromDjango);
            }
            
            closeEditModal();
            showNotification('Profile updated successfully!', 'success');
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Error saving profile:', error);
        showNotification('Error saving profile. Please try again.', 'error');
    }
}

// ============================================
// UPDATE DISPLAY FUNCTIONS
// ============================================

function updateProfileDisplay(updatedData) {
    console.log('🔥 Updating display with:', updatedData);
    
    // Update the page display immediately
    if (updatedData.name) {
        document.getElementById('displayName').textContent = updatedData.name;
    }
    if (updatedData.title) {
        document.getElementById('displayTitle').textContent = updatedData.title;
    }
    if (updatedData.school) {
        document.getElementById('displaySchool').textContent = updatedData.school;
    }
    if (updatedData.year) {
        document.getElementById('displayYear').textContent = updatedData.year;
    }
    if (updatedData.location) {
        document.getElementById('displayLocation').textContent = updatedData.location;
    }
    if (updatedData.graduation) {
        document.getElementById('displayGraduation').textContent = updatedData.graduation;
    }
    if (updatedData.about) {
        document.getElementById('displayAbout').textContent = updatedData.about;
    }
    if (updatedData.specialization) {
        document.getElementById('displaySpecialization').textContent = updatedData.specialization;
    }
    if (updatedData.major) {
        document.getElementById('displayMajor').textContent = updatedData.major;
    }
    if (updatedData.minor) {
        document.getElementById('displayMinor').textContent = updatedData.minor;
    }
    
    // Update courses display
    const coursesEl = document.getElementById('displayCourses');
    if (updatedData.courses && updatedData.courses.trim()) {
        const coursesArray = updatedData.courses.split(',').map(c => c.trim());
        coursesEl.innerHTML = coursesArray.map(course => 
            `<span class="tag">${course}</span>`
        ).join('');
    } else {
        coursesEl.innerHTML = '<span class="tag tag-empty">No courses listed</span>';
    }
    
    // Update interests
    if (updatedData.interests) {
        document.getElementById('displayInterests').textContent = updatedData.interests;
    }
}

// ============================================
// MODAL FUNCTIONS
// ============================================

function openEditModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Populate form with current data from global profileData
    if (window.profileDataFromDjango) {
        document.getElementById('name').value = window.profileDataFromDjango.name || '';
        document.getElementById('title').value = window.profileDataFromDjango.title || '';
        document.getElementById('school').value = window.profileDataFromDjango.school || '';
        document.getElementById('year').value = window.profileDataFromDjango.year || '';
        document.getElementById('location').value = window.profileDataFromDjango.location || '';
        document.getElementById('about').value = window.profileDataFromDjango.about || '';
        document.getElementById('graduation').value = window.profileDataFromDjango.graduation || '';
        document.getElementById('specialization').value = window.profileDataFromDjango.specialization || '';
        document.getElementById('major').value = window.profileDataFromDjango.major || '';
        document.getElementById('minor').value = window.profileDataFromDjango.minor || '';
        document.getElementById('courses').value = window.profileDataFromDjango.courses || '';
        document.getElementById('interests').value = window.profileDataFromDjango.interests || '';
    }
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// ============================================
// EVENT LISTENERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔥 userProfile.js loaded');
    console.log('🔥 Profile data available:', window.profileDataFromDjango);
    
    // Set up form submission
    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', saveProfile);
    }
    
    // Close modal when clicking outside
    const editModal = document.getElementById('editModal');
    if (editModal) {
        editModal.addEventListener('click', function(e) {
            if (e.target === editModal) {
                closeEditModal();
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        const editModal = document.getElementById('editModal');
        if (e.key === 'Escape' && editModal && editModal.style.display === 'flex') {
            closeEditModal();
        }
    });
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);