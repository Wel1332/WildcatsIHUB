// Filter and Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const projectsGrid = document.getElementById('projectsGrid');
    const filterOptions = document.querySelectorAll('.filter-option input[type="radio"]');
    const searchBtn = document.querySelector('.search-btn');
    
    // Filter projects by category
    filterOptions.forEach(option => {
        option.addEventListener('change', function() {
            const category = this.parentElement.getAttribute('data-category');
            filterProjects(category);
        });
    });
    
    // Search functionality
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    function filterProjects(category) {
        const projectCards = document.querySelectorAll('.project-card');
        
        projectCards.forEach(card => {
            if (category === 'all' || card.getAttribute('data-category') === category) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const projectCards = document.querySelectorAll('.project-card');
        
        if (!searchTerm) {
            // If search is empty, show all projects
            projectCards.forEach(card => {
                card.style.display = 'block';
            });
            return;
        }
        
        projectCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('p').textContent.toLowerCase();
            const author = card.querySelector('.author-name').textContent.toLowerCase();
            const major = card.querySelector('.author-major').textContent.toLowerCase();
            
            // Search in title, description, author name, and major
            const matches = title.includes(searchTerm) || 
                           description.includes(searchTerm) || 
                           author.includes(searchTerm) || 
                           major.includes(searchTerm);
            
            if (matches) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Add click handlers for view project buttons
    const viewButtons = document.querySelectorAll('.view-project-btn');
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const projectTitle = this.closest('.project-card').querySelector('h3').textContent;
            alert(`Viewing project: ${projectTitle}\n\nThis would navigate to the project details page in a real application.`);
        });
    });
});