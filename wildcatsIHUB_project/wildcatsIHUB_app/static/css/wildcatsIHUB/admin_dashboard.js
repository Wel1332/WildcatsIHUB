document.addEventListener('DOMContentLoaded', () => {

  // ===== Fade-up animations =====
  const fadeElements = document.querySelectorAll('.fade-up');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.15 }
  );
  fadeElements.forEach(el => observer.observe(el));

  // ===== Approvals tabs =====
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      tabs.forEach(t => t.classList.remove('active'));
      e.currentTarget.classList.add('active');

      // filter cards
      const filter = e.currentTarget.textContent.toLowerCase().split(' ')[0];
      const cards = document.querySelectorAll('.project-card');
      cards.forEach(c => {
        if (filter === 'pending') {
          c.style.display = 'block';
        } else if (filter === 'approved') {
          c.style.display = c.querySelector('.btn-primary') ? 'none' : 'block';
        } else if (filter === 'rejected') {
          c.style.display = c.querySelector('.btn-danger') ? 'none' : 'block';
        }
      });
    });
  });

  // ===== Search input filtering =====
  const searchInputs = document.querySelectorAll('.search-input');
  searchInputs.forEach(input => {
    input.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      const tableRows = e.target.closest('.card').querySelectorAll('tbody tr');
      tableRows.forEach(row => {
        let text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  });

  // ===== Chart rendering (admin_dashboard) =====
  const chartEl = document.getElementById('projectChart');
  const dataEl = document.getElementById('chart-data');
  if (chartEl && dataEl) {
    try {
      const payload = JSON.parse(dataEl.textContent);
      const ctx = chartEl.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: payload.months || [],
          datasets: [{
            label: 'Projects Created',
            data: payload.projectData || [],
            borderColor: '#1e5cff',
            backgroundColor: 'rgba(30,92,255,0.08)',
            borderWidth: 3,
            tension: 0.35,
            fill: true,
            pointBackgroundColor: '#155DFD'
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true } }
        }
      });
    } catch (err) {
      console.error('Failed to parse chart data', err);
    }
  }

});
