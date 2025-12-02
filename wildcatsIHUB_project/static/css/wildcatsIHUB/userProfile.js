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
// AVATAR INITIALS FUNCTIONS
// ============================================

function updateAvatarInitials(name) {
    const avatarElement = document.getElementById('avatarInitials');
    if (!avatarElement) return;
    
    if (name && name.trim()) {
        // Get initials from name
        const initials = getInitialsFromName(name);
        avatarElement.textContent = initials;
        
        // Add random color for avatar (based on name for consistency)
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
        ];
        
        // Use consistent color based on name hash
        const colorIndex = hashCode(name) % colors.length;
        avatarElement.style.background = colors[colorIndex];
    } else {
        avatarElement.textContent = '?';
        avatarElement.style.background = '#9ca3af';
    }
}

function getInitialsFromName(name) {
    if (!name) return '?';
    
    const nameParts = name.trim().split(' ');
    
    if (nameParts.length === 1) {
        // Single name: take first 2 letters
        return nameParts[0].substring(0, 2).toUpperCase();
    } else {
        // Multiple names: take first letter of first and last name
        return (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
    }
}

function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return Math.abs(hash);
}

// ============================================
// SAVE DATA TO SUPABASE - UPDATED WITH DEBUGGING
// ============================================

async function saveProfile(event) {
    event.preventDefault();
    
    try {
        console.log('🔄 Starting profile save...');
        
        // Show loading state
        const saveBtn = document.querySelector('#editProfileForm button[type="submit"]');
        const originalBtnText = saveBtn ? saveBtn.textContent : 'Save Changes';
        if (saveBtn) {
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            saveBtn.disabled = true;
        }
        
        // Get form values - USING CORRECT SUPABASE COLUMN NAMES
        const formData = new FormData();
        
        // Add all form fields with EXACT column names
        formData.append('full_name', document.getElementById('name').value);
        formData.append('title', document.getElementById('title').value);
        formData.append('school', document.getElementById('school').value);
        formData.append('year_level', document.getElementById('year').value);  // year_level column
        formData.append('location', document.getElementById('location').value);
        formData.append('graduation_year', document.getElementById('graduation').value);  // graduation_year column
        formData.append('about', document.getElementById('about').value);
        formData.append('specialization', document.getElementById('specialization').value);
        formData.append('major', document.getElementById('major').value);
        formData.append('minor', document.getElementById('minor').value);
        formData.append('courses', document.getElementById('courses').value);
        formData.append('interests', document.getElementById('interests').value);
        
        // Also add first_name and last_name for auth_user table
        const fullName = document.getElementById('name').value;
        if (fullName) {
            const nameParts = fullName.trim().split(' ');
            if (nameParts.length >= 2) {
                formData.append('first_name', nameParts[0]);
                formData.append('last_name', nameParts.slice(1).join(' '));
            } else {
                formData.append('first_name', fullName);
                formData.append('last_name', '');
            }
        }
        
        // Debug: Log what we're sending
        console.log('📤 SENDING PROFILE DATA TO SERVER:');
        const formDataObj = {};
        for (let [key, value] of formData.entries()) {
            formDataObj[key] = value;
            console.log(`  ${key}: ${value}`);
        }
        
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
        console.log('📥 SERVER RESPONSE:', result);
        
        // Reset button
        if (saveBtn) {
            saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Changes';
            saveBtn.disabled = false;
        }
        
        if (result.success) {
            console.log('✅ Profile saved successfully!');
            
            // Update local profile data
            const updatedData = {
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
            
            // Update window.profileDataFromDjango
            window.profileDataFromDjango = { ...window.profileDataFromDjango, ...updatedData };
            
            console.log('🔄 Updated window.profileDataFromDjango:', window.profileDataFromDjango);
            
            // Update the display including avatar
            updateProfileDisplay(updatedData);
            
            closeEditModal();
            showNotification('Profile saved successfully!', 'success');
            
            // Force page refresh after 2 seconds to ensure everything syncs
            setTimeout(() => {
                console.log('🔄 Refreshing page to sync data...');
                location.reload();
            }, 2000);
            
        } else {
            throw new Error(result.message || 'Server returned error');
        }
        
    } catch (error) {
        console.error('❌ ERROR SAVING PROFILE:', error);
        showNotification('Error: ' + error.message, 'error');
        
        // Reset button on error
        const saveBtn = document.querySelector('#editProfileForm button[type="submit"]');
        if (saveBtn) {
            saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Changes';
            saveBtn.disabled = false;
        }
    }
}

// ============================================
// UPDATE DISPLAY FUNCTIONS
// ============================================

function updateProfileDisplay(updatedData) {
    console.log('🔥 Updating display with:', updatedData);
    
    // Helper function to safely update element
    function updateElement(id, value, fallback = 'Not specified') {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value && value.trim() ? value : fallback;
        }
    }
    
    // Update all display elements
    updateElement('displayName', updatedData.name, 'No name set');
    updateElement('displayTitle', updatedData.title, 'No title set');
    updateElement('displaySchool', updatedData.school, 'School not specified');
    updateElement('displayYear', updatedData.year, 'Year level not specified');
    updateElement('displayLocation', updatedData.location, 'Location not specified');
    updateElement('displayGraduation', updatedData.graduation, 'Graduation year not specified');
    updateElement('displayAbout', updatedData.about, 'No about information');
    updateElement('displaySpecialization', updatedData.specialization, 'No specialization');
    updateElement('displayMajor', updatedData.major, 'Major not specified');
    updateElement('displayMinor', updatedData.minor, 'Minor not specified');
    
    // Update avatar initials
    updateAvatarInitials(updatedData.name);
    
    // Update courses (special handling for tags)
    const coursesEl = document.getElementById('displayCourses');
    if (coursesEl) {
        if (updatedData.courses && updatedData.courses.trim()) {
            const coursesArray = updatedData.courses.split(',').map(c => c.trim()).filter(c => c);
            if (coursesArray.length > 0) {
                coursesEl.innerHTML = coursesArray.map(course => 
                    `<span class="tag">${course}</span>`
                ).join('');
            } else {
                coursesEl.innerHTML = '<span class="tag tag-empty">No courses listed</span>';
            }
        } else {
            coursesEl.innerHTML = '<span class="tag tag-empty">No courses listed</span>';
        }
    }
    
    // Update interests
    updateElement('displayInterests', updatedData.interests, 'No interests listed');
    
    console.log('✅ Display updated successfully');
}

// ============================================
// MODAL FUNCTIONS
// ============================================

function openEditModal() {
    const modal = document.getElementById('editModal');
    if (!modal) {
        console.error('❌ Edit modal not found!');
        return;
    }
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    console.log('📝 Opening edit modal with data:', window.profileDataFromDjango);
    
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
    } else {
        console.warn('⚠️ No profileDataFromDjango available');
    }
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
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
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// ============================================
// EVENT LISTENERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔥 userProfile.js loaded successfully');
    console.log('📊 Profile data available:', window.profileDataFromDjango);
    
    // Set up form submission
    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        console.log('✅ Edit profile form found');
        editProfileForm.addEventListener('submit', saveProfile);
    } else {
        console.error('❌ Edit profile form NOT found!');
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
    
    // Initialize avatar on page load
    if (window.profileDataFromDjango && window.profileDataFromDjango.name) {
        updateAvatarInitials(window.profileDataFromDjango.name);
    }
    
    console.log('✅ All event listeners set up');
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
    
    .tag {
        display: inline-block;
        background: #e2e8f0;
        color: #4a5568;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        margin: 2px;
    }
    
    .tag-empty {
        background: #fed7d7;
        color: #742a2a;
    }
    
    .fa-spin {
        animation: fa-spin 1s infinite linear;
    }
    
    @keyframes fa-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Avatar initials styles */
    #avatarInitials {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        border: 4px solid white;
        transition: transform 0.3s ease;
        cursor: default;
    }
    
    #avatarInitials:hover {
        transform: scale(1.03);
    }
`;
document.head.appendChild(style);

console.log('✅ userProfile.js loaded and ready!');