
        // Sidebar toggle functionality
        const menuToggle = document.querySelector('.menu-toggle');
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        const overlay = document.querySelector('.sidebar-overlay');
        
        menuToggle?.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-active');
            
            // Add overlay when sidebar is active on mobile
            if (window.innerWidth <= 768) {
                if (sidebar.classList.contains('active')) {
                    overlay.classList.add('active');
                    document.body.style.overflow = 'hidden';
                } else {
                    overlay.classList.remove('active');
                    document.body.style.overflow = '';
                }
            }
        });

        // Close sidebar when clicking overlay
        overlay?.addEventListener('click', () => {
            sidebar.classList.remove('active');
            mainContent.classList.remove('sidebar-active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        });

        // Close sidebar when clicking outside on desktop
        document.addEventListener('click', (e) => {
            if (window.innerWidth > 768 && 
                sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                mainContent.classList.remove('sidebar-active');
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Your existing animations code
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.feed-item, .action-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });

        // Enhanced hover effects for buttons
        document.querySelectorAll('.action-card, .new-btn, .filter-btn, .star-btn').forEach(button => {
            button.addEventListener('mouseenter', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const ripple = document.createElement('span');
                ripple.style.cssText = `
                    position: absolute;
                    top: ${y}px;
                    left: ${x}px;
                    width: 0;
                    height: 0;
                    border-radius: 50%;
                    background: rgba(30, 92, 255, 0.1);
                    transform: translate(-50%, -50%);
                    animation: ripple 0.6s ease-out;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });

        // Search functionality
        const searchUsersInput = document.querySelector('.search-users-input');
        searchUsersInput?.addEventListener('focus', function() {
            this.parentElement.style.boxShadow = '0 0 0 3px rgba(30, 92, 255, 0.2), 0 8px 24px rgba(0, 0, 0, 0.15)';
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        searchUsersInput?.addEventListener('blur', function() {
            this.parentElement.style.boxShadow = '';
            this.parentElement.style.transform = '';
        });
