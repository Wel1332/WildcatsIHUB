// ============================================
// Professional Student Profile JavaScript
// ============================================

// Profile data storage
let profileData = {
    name: '',
    title: '',
    school: '',
    year: '',
    location: '',
    about: '',
    graduation: '',
    specialization: '',
    major: '',
    minor: '',
    courses: '',
    interests: ''
};

// Skills tracking
let skillsData = {};

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
// LOAD DATA FROM SUPABASE VIA DJANGO
// ============================================

async function loadUserProfile() {
    try {
        const response = await fetch('/user-profile/data/');
        const result = await response.json();
        
        if (result.success && result.data) {
            // Update profileData with real data from Supabase
            profileData = {
                name: result.data.full_name || '',
                title: result.data.title || '',
                school: result.data.school || '',
                year: result.data.year_level || '',
                location: result.data.location || '',
                about: result.data.about || '',
                graduation: result.data.graduation_year || '',
                specialization: result.data.specialization || '',
                major: result.data.major || '',
                minor: result.data.minor || '',
                courses: result.data.courses || '',
                interests: result.data.interests || ''
            };
            
            // Update display with real data
            updateDisplay();
        } else {
            // Use default empty data if no profile found
            updateDisplay();
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
        // Fallback to empty data
        updateDisplay();
    }
}

// ============================================
// SAVE DATA TO SUPABASE VIA DJANGO
// ============================================

async function saveProfile(event) {
    event.preventDefault();
    
    try {
        // Get form values
        const formData = new FormData();
        formData.append('name', document.getElementById('name').value);
        formData.append('title', document.getElementById('title').value);
        formData.append('school', document.getElementById('school').value);
        formData.append('year', document.getElementById('year').value);
        formData.append('location', document.getElementById('location').value);
        formData.append('about', document.getElementById('about').value);
        formData.append('graduation', document.getElementById('graduation').value);
        formData.append('specialization', document.getElementById('specialization').value);
        formData.append('major', document.getElementById('major').value);
        formData.append('minor', document.getElementById('minor').value);
        formData.append('courses', document.getElementById('courses').value);
        formData.append('interests', document.getElementById('interests').value);
        
        const response = await fetch('/user-profile/save/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData
        });

        const result = await response.json();
        
        if (result.success) {
            // Update profileData with new values
            profileData = {
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
            
            // Update display
            updateDisplay();
            
            // Close modal
            closeEditModal();
            
            // Show success message
            showNotification('Profile updated successfully in Supabase!', 'success');
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Error saving profile:', error);
        showNotification('Error saving profile. Please try again.', 'error');
    }
}

async function saveProject(event) {
    event.preventDefault();
    
    try {
        const formData = new FormData();
        formData.append('projectName', document.getElementById('projectName').value);
        formData.append('projectDescription', document.getElementById('projectDescription').value);
        formData.append('projectLanguages', document.getElementById('projectLanguages').value);
        formData.append('projectDate', document.getElementById('projectDate').value);
        formData.append('projectLink', document.getElementById('projectLink').value);
        
        const response = await fetch('/user-profile/save-project/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData
        });

        const result = await response.json();
        
        if (result.success) {
            // Reload the page to show the new project from database
            location.reload();
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Error saving project:', error);
        showNotification('Error saving project. Please try again.', 'error');
    }
}

// ============================================
// MODAL FUNCTIONS
// ============================================

function openEditModal() {
    const modal = document.getElementById('editModal');
    modal.classList.add('active');
    modal.style.display = 'flex';
    
    // Populate form with current real data
    document.getElementById('name').value = profileData.name;
    document.getElementById('title').value = profileData.title;
    document.getElementById('school').value = profileData.school;
    document.getElementById('year').value = profileData.year;
    document.getElementById('location').value = profileData.location;
    document.getElementById('about').value = profileData.about;
    document.getElementById('graduation').value = profileData.graduation;
    document.getElementById('specialization').value = profileData.specialization;
    document.getElementById('major').value = profileData.major;
    document.getElementById('minor').value = profileData.minor;
    document.getElementById('courses').value = profileData.courses;
    document.getElementById('interests').value = profileData.interests;
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    modal.classList.remove('active');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 200);
    
    // Restore body scroll
    document.body.style.overflow = '';
}

function openProjectModal() {
    const modal = document.getElementById('projectModal');
    modal.classList.add('active');
    modal.style.display = 'flex';
    
    // Reset form
    document.getElementById('addProjectForm').reset();
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeProjectModal() {
    const modal = document.getElementById('projectModal');
    modal.classList.remove('active');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 200);
    
    // Restore body scroll
    document.body.style.overflow = '';
}

// ============================================
// UPDATE DISPLAY FUNCTIONS
// ============================================

function updateDisplay() {
    // Header information
    document.getElementById('displayName').textContent = profileData.name;
    document.getElementById('displayTitle').textContent = profileData.title;
    document.getElementById('displaySchool').textContent = profileData.school;
    document.getElementById('displayYear').textContent = profileData.year;
    
    // Location
    const locationEl = document.getElementById('displayLocation');
    locationEl.textContent = profileData.location || 'Add location';
    
    // Graduation
    const graduationEl = document.getElementById('displayGraduation');
    graduationEl.textContent = profileData.graduation || 'Add graduation year';
    
    // About section
    const aboutEl = document.getElementById('displayAbout');
    aboutEl.textContent = profileData.about || 'Add information about yourself...';
    
    // Specialization
    const specializationEl = document.getElementById('displaySpecialization');
    specializationEl.textContent = profileData.specialization || 'Add specialization';
    
    // Academic information
    document.getElementById('displayMajor').textContent = profileData.major || 'Add major';
    document.getElementById('displayMinor').textContent = profileData.minor || 'Not specified';
    
    // Courses
    const coursesEl = document.getElementById('displayCourses');
    if (profileData.courses && profileData.courses.trim()) {
        const coursesArray = profileData.courses.split(',').map(c => c.trim());
        coursesEl.innerHTML = coursesArray.map(course => 
            `<span class="tag">${course}</span>`
        ).join('');
    } else {
        coursesEl.innerHTML = '<span class="tag">No courses added</span>';
    }
    
    // Interests
    const interestsEl = document.getElementById('displayInterests');
    interestsEl.textContent = profileData.interests || 'No interests specified';
}

function updateSkillsDisplay() {
    const skillsEl = document.getElementById('skillsProgressList');
    
    // This will be populated from projects data
    const skillsArray = Object.entries(skillsData).sort((a, b) => b[1].count - a[1].count);
    
    if (skillsArray.length === 0) {
        skillsEl.innerHTML = `
            <div class="empty-state-card">
                <i class="fas fa-code"></i>
                <p>Add projects to track your skill growth!</p>
            </div>
        `;
        return;
    }
    
    skillsEl.innerHTML = skillsArray.map(([skill, data]) => {
        const level = getSkillLevel(data.count);
        const percentage = Math.min((data.count / 5) * 100, 100);
        
        return `
            <div class="skill-item">
                <div class="skill-header">
                    <span class="skill-name">${skill}</span>
                    <span class="skill-level">${level}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }).join('');
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function getSkillLevel(count) {
    if (count >= 5) return 'Expert';
    if (count >= 3) return 'Advanced';
    if (count >= 2) return 'Intermediate';
    return 'Beginner';
}

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
    // Load real data from Supabase when page loads
    loadUserProfile();
    
    // Close modals when clicking outside (but not on the modal content)
    const editModal = document.getElementById('editModal');
    const projectModal = document.getElementById('projectModal');
    const editModalContent = editModal.querySelector('.modal-content');
    const projectModalContent = projectModal.querySelector('.modal-content');
    
    // Close modals when clicking on overlay
    editModal.addEventListener('click', function(e) {
        if (e.target === editModal) {
            closeEditModal();
        }
    });
    
    projectModal.addEventListener('click', function(e) {
        if (e.target === projectModal) {
            closeProjectModal();
        }
    });
    
    // Prevent clicks inside modal content from closing the modal
    editModalContent.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    projectModalContent.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Close modals with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (editModal.classList.contains('active')) {
                closeEditModal();
            }
            if (projectModal.classList.contains('active')) {
                closeProjectModal();
            }
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