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
    clubs: '',
    projects: '',
    interests: ''
};

// Open modal
function openEditModal() {
    const modal = document.getElementById('editModal');
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
    document.getElementById('clubs').value = profileData.clubs;
    document.getElementById('projects').value = profileData.projects;
    document.getElementById('interests').value = profileData.interests;
}

// Close modal
function closeEditModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = 'none';
}

// Save profile
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
    profileData.clubs = document.getElementById('clubs').value;
    profileData.projects = document.getElementById('projects').value;
    profileData.interests = document.getElementById('interests').value;
    
    // Update display
    updateDisplay();
    
    // Close modal
    closeEditModal();
}

// Update display with saved data
function updateDisplay() {
    // Header information
    document.getElementById('displayName').textContent = profileData.name;
    document.getElementById('displayTitle').textContent = profileData.title;
    document.getElementById('displaySchool').textContent = profileData.school;
    document.getElementById('displayYear').textContent = profileData.year;
    
    // About section
    const aboutEl = document.getElementById('displayAbout');
    if (profileData.about) {
        aboutEl.textContent = profileData.about;
        aboutEl.classList.remove('empty-state');
    } else {
        aboutEl.textContent = 'No information added yet';
        aboutEl.classList.add('empty-state');
    }
    
    const locationEl = document.getElementById('displayLocation');
    if (profileData.location) {
        locationEl.textContent = profileData.location;
        locationEl.classList.remove('empty-state');
    } else {
        locationEl.textContent = 'Add location';
        locationEl.classList.add('empty-state');
    }
    
    const graduationEl = document.getElementById('displayGraduation');
    if (profileData.graduation) {
        graduationEl.textContent = profileData.graduation;
        graduationEl.classList.remove('empty-state');
    } else {
        graduationEl.textContent = 'Add graduation year';
        graduationEl.classList.add('empty-state');
    }
    
    const specializationEl = document.getElementById('displaySpecialization');
    if (profileData.specialization) {
        specializationEl.textContent = profileData.specialization;
        specializationEl.classList.remove('empty-state');
    } else {
        specializationEl.textContent = 'Add specialization';
        specializationEl.classList.add('empty-state');
    }
    
    // Academic information
    document.getElementById('displayMajor').textContent = profileData.major;
    
    const minorEl = document.getElementById('displayMinor');
    if (profileData.minor) {
        minorEl.textContent = profileData.minor;
        minorEl.classList.remove('empty-state');
    } else {
        minorEl.textContent = 'Not specified';
        minorEl.classList.add('empty-state');
    }
    
    const coursesEl = document.getElementById('displayCourses');
    if (profileData.courses) {
        const coursesArray = profileData.courses.split(',').map(c => c.trim());
        coursesEl.innerHTML = coursesArray.map(course => 
            `<span class="course-tag">${course}</span>`
        ).join('');
        coursesEl.classList.remove('empty-state');
    } else {
        coursesEl.textContent = 'No courses added';
        coursesEl.classList.add('empty-state');
    }
    
    // Campus involvement
    const clubsEl = document.getElementById('displayClubs');
    if (profileData.clubs) {
        clubsEl.textContent = profileData.clubs;
        clubsEl.classList.remove('empty-state');
    } else {
        clubsEl.textContent = 'No club information added';
        clubsEl.classList.add('empty-state');
    }
    
    // Projects
    const projectsEl = document.getElementById('displayProjects');
    if (profileData.projects) {
        projectsEl.textContent = profileData.projects;
        projectsEl.classList.remove('empty-state');
    } else {
        projectsEl.textContent = 'No projects added yet';
        projectsEl.classList.add('empty-state');
    }
    
    // Interests
    const interestsEl = document.getElementById('displayInterests');
    if (profileData.interests) {
        interestsEl.textContent = profileData.interests;
        interestsEl.classList.remove('empty-state');
    } else {
        interestsEl.textContent = 'No interests specified';
        interestsEl.classList.add('empty-state');
    }
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('editModal');
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeEditModal();
        }
    });
    
    // Initialize display on page load
    updateDisplay();
});