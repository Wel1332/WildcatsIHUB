// ============================================
// Professional Student Profile JavaScript
// ============================================

// Profile data storage
let profileData = {
    name: 'Sarah Chen',
    title: 'Computer Science Major',
    school: 'Stanford University',
    year: '2nd',
    location: '',
    about: '',
    graduation: '',
    specialization: '',
    major: 'Computer Science',
    minor: '',
    courses: '',
    interests: ''
};


// Skills tracking
let skillsData = {};

// ============================================
// MODAL FUNCTIONS
// ============================================

function openEditModal() {
    const modal = document.getElementById('editModal');
    modal.classList.add('active');
    modal.style.display = 'flex';
    
    // Populate form with current data
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
// SAVE FUNCTIONS
// ============================================

function saveProfile(event) {
    event.preventDefault();
    
    // Get form values
    profileData.name = document.getElementById('name').value || 'Sarah Chen';
    profileData.title = document.getElementById('title').value || 'Computer Science Major';
    profileData.school = document.getElementById('school').value || 'Stanford University';
    profileData.year = document.getElementById('year').value || '2nd';
    profileData.location = document.getElementById('location').value;
    profileData.about = document.getElementById('about').value;
    profileData.graduation = document.getElementById('graduation').value;
    profileData.specialization = document.getElementById('specialization').value;
    profileData.major = document.getElementById('major').value || 'Computer Science';
    profileData.minor = document.getElementById('minor').value;
    profileData.courses = document.getElementById('courses').value;
    profileData.interests = document.getElementById('interests').value;
    
    // Update display
    updateDisplay();
    
    // Close modal with animation
    closeEditModal();
    
    // Show success message
    showNotification('Profile updated successfully!', 'success');
}

function saveProject(event) {
    event.preventDefault();
    
    // Get form values
    const projectName = document.getElementById('projectName').value;
    const projectDescription = document.getElementById('projectDescription').value;
    const projectLanguages = document.getElementById('projectLanguages').value;
    const projectDate = document.getElementById('projectDate').value;
    const projectLink = document.getElementById('projectLink').value;
    
    // Create project object
    const project = {
        id: Date.now(),
        name: projectName,
        description: projectDescription,
        technologies: projectLanguages.split(',').map(tech => tech.trim()),
        date: projectDate,
        link: projectLink
    };
    
    // Add to projects array
    projects.push(project);
    
    // Update skills tracking
    updateSkillsFromProject(project.technologies);
    
    // Update display
    updateSkillsDisplay();
    
    // Close modal
    closeProjectModal();
    
    // Show success message
    showNotification('Project added successfully!', 'success');
}

function deleteProject(projectId) {
    if (confirm('Are you sure you want to delete this project?')) {
        // Find project index
        const index = projects.findIndex(p => p.id === projectId);
        
        if (index !== -1) {
            // Remove technologies from skills tracking
            const technologies = projects[index].technologies;
            technologies.forEach(tech => {
                if (skillsData[tech]) {
                    skillsData[tech].count--;
                    if (skillsData[tech].count <= 0) {
                        delete skillsData[tech];
                    }
                }
            });
            
            // Remove project
            projects.splice(index, 1);
            
            // Update displays
        

            updateSkillsDisplay();
            
            // Show success message
            showNotification('Project deleted successfully!', 'success');
        }
    }
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
    document.getElementById('displayMajor').textContent = profileData.major;
    document.getElementById('displayMinor').textContent = profileData.minor || 'Not specified';
    
    // Courses
    const coursesEl = document.getElementById('displayCourses');
    if (profileData.courses) {
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

function updateProjectsDisplay() {
    const projectsEl = document.getElementById('displayProjects');
    
    if (projects.length === 0) {
        projectsEl.innerHTML = `
            <div class="empty-state-card">
                <i class="fas fa-folder-plus"></i>
                <p>No projects added yet</p>
                <small>Click "Add Project" to get started!</small>
            </div>
        `;
        return;
    }
    
    projectsEl.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="project-header">
                <div>
                    <h4 class="project-title">${project.name}</h4>
                    ${project.date ? `<p class="project-date">${formatDate(project.date)}</p>` : ''}
                </div>
            </div>
            <p class="project-description">${project.description}</p>
            <div class="project-technologies">
                ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
            </div>
            <div class="project-footer">
                ${project.link ? `<a href="${project.link}" target="_blank" class="project-link"><i class="fas fa-external-link-alt"></i> View Project</a>` : '<span></span>'}
                <button class="delete-project-btn" onclick="deleteProject(${project.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        </div>
    `).join('');
}

function updateSkillsDisplay() {
    const skillsEl = document.getElementById('skillsProgressList');
    
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

function updateSkillsFromProject(technologies) {
    technologies.forEach(tech => {
        if (!skillsData[tech]) {
            skillsData[tech] = { count: 0 };
        }
        skillsData[tech].count++;
    });
}

function getSkillLevel(count) {
    if (count >= 5) return 'Expert';
    if (count >= 3) return 'Advanced';
    if (count >= 2) return 'Intermediate';
    return 'Beginner';
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString + '-01');
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
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
// EVENT LISTENERS - FIXED MODAL CLOSING ISSUE
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize display
    updateDisplay();
 
    updateSkillsDisplay();
    
    // Close modals when clicking outside (but not on the modal content)
    const editModal = document.getElementById('editModal');
    const projectModal = document.getElementById('projectModal');
    const editModalContent = editModal.querySelector('.modal-content');
    const projectModalContent = projectModal.querySelector('.modal-content');
    
    
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