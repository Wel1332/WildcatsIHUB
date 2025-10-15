const sidebar = document.getElementById('sidebar');
const collapseBtn = document.getElementById('collapse-btn');

collapseBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    lucide.replace(); // Refresh Lucide icons
});