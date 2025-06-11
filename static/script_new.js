// Modern Vietnamese Food Recommendation System - Enhanced UI
// Author: AI Assistant
// Version: 2.0

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 DOM loaded, starting modern initialization...');

    // Initialize modern UI components
    try {
        initModernUI();
        initDarkMode();
        initSmoothTransitions();
        initFormValidation();
        console.log('✅ Basic features initialized');

        // Initialize customer selection with enhanced features
        setTimeout(() => {
            try {
                initModernCustomerSelection();
                console.log('✅ Modern customer selection initialized');
            } catch (error) {
                console.error('❌ Customer selection error:', error);
            }
        }, 500);

    } catch (error) {
        console.error('❌ Initialization error:', error);
    }

    // Initialize navbar and navigation
    initModernNavbar();

    // Initialize form handling
    initEnhancedFormHandling();

    // Initialize particles effect
    createParticlesEffect();

    // Show welcome message
    setTimeout(() => {
        showModernToast('🍽️ Chào mừng đến với hệ thống gợi ý món ăn!', 'success', 4000);
    }, 1000);
});

// Modern Customer Selection with Enhanced UX
function initModernCustomerSelection() {
    console.log('Initializing modern customer selection...');

    const userIdSelect = document.getElementById('userId');
    const customerInfo = document.getElementById('customerInfo');
    const randomBtn = document.getElementById('randomCustomer');
    const firstBtn = document.getElementById('firstCustomer');
    const vipBtn = document.getElementById('vipCustomer');
    const toggleSearchBtn = document.getElementById('toggleSearch');
    const searchBox = document.getElementById('customerSearchBox');
    const searchInput = document.getElementById('customerSearch');
    const searchResults = document.getElementById('searchResults');

    if (!userIdSelect) {
        console.error('User select element not found!');
        return;
    }

    // Enhanced toggle search with smooth animations
    if (toggleSearchBtn && searchBox) {
        toggleSearchBtn.addEventListener('click', function () {
            searchBox.classList.toggle('active');
            const isActive = searchBox.classList.contains('active');

            // Update button with smooth transition
            this.innerHTML = isActive
                ? '<i class="fas fa-times me-1"></i>Đóng'
                : '<i class="fas fa-search me-1"></i>Tìm kiếm';

            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => this.style.transform = '', 150);

            if (isActive && searchInput) {
                setTimeout(() => {
                    searchInput.focus();
                    searchInput.placeholder = 'Nhập ID hoặc tên khách hàng...';
                }, 300);
            }
        });
    }

    // Enhanced search with real-time suggestions
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();
            if (query.length < 2) {
                searchResults.innerHTML = '';
                return;
            }

            const options = Array.from(userIdSelect.querySelectorAll('option[value!=""]'));
            const matches = options.filter(option =>
                option.textContent.toLowerCase().includes(query) ||
                option.value.toLowerCase().includes(query)
            );

            // Create enhanced search results
            searchResults.innerHTML = matches.length ?
                matches.slice(0, 8).map((option, index) => `
                    <div class="search-result-item" data-value="${option.value}" style="animation-delay: ${index * 50}ms">
                        <i class="fas fa-user me-2"></i>
                        <span class="result-text">${option.textContent}</span>
                        <i class="fas fa-chevron-right ms-auto"></i>
                    </div>
                `).join('') :
                '<div class="search-result-item no-results"><i class="fas fa-search me-2"></i>Không tìm thấy khách hàng</div>';

            // Add click handlers with enhanced feedback
            searchResults.querySelectorAll('.search-result-item[data-value]').forEach(item => {
                item.addEventListener('click', function () {
                    const value = this.getAttribute('data-value');
                    const text = this.querySelector('.result-text').textContent;

                    // Smooth selection with visual feedback
                    this.style.background = '#667eea';
                    this.style.color = 'white';

                    setTimeout(() => {
                        userIdSelect.value = value;
                        updateEnhancedCustomerInfo(value, text);
                        searchInput.value = '';
                        searchResults.innerHTML = '';
                        searchBox.classList.remove('active');
                        toggleSearchBtn.innerHTML = '<i class="fas fa-search me-1"></i>Tìm kiếm';
                        showModernToast('✅ Đã chọn: ' + text, 'success');
                    }, 200);
                });

                // Add hover effects
                item.addEventListener('mouseenter', function () {
                    this.style.transform = 'translateX(5px)';
                });

                item.addEventListener('mouseleave', function () {
                    this.style.transform = 'translateX(0)';
                });
            });
        });

        // Enhanced keyboard navigation
        searchInput.addEventListener('keydown', function (e) {
            const items = searchResults.querySelectorAll('.search-result-item[data-value]');
            if (items.length === 0) return;

            let currentIndex = Array.from(items).findIndex(item => item.classList.contains('highlighted'));

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                currentIndex = (currentIndex + 1) % items.length;
                highlightSearchItem(items, currentIndex);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                currentIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                highlightSearchItem(items, currentIndex);
            } else if (e.key === 'Enter' && currentIndex >= 0) {
                e.preventDefault();
                items[currentIndex].click();
            }
        });
    }

    // Enhanced quick selection buttons
    if (randomBtn) {
        randomBtn.addEventListener('click', function () {
            const options = userIdSelect.querySelectorAll('option[value!=""]');
            if (options.length > 0) {
                const randomOption = options[Math.floor(Math.random() * options.length)];

                // Add loading effect
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang chọn...';
                this.disabled = true;

                setTimeout(() => {
                    userIdSelect.value = randomOption.value;
                    updateEnhancedCustomerInfo(randomOption.value, randomOption.textContent);
                    showModernToast('🎲 Đã chọn khách hàng ngẫu nhiên!', 'success');

                    // Reset button
                    this.innerHTML = '<i class="fas fa-random me-1"></i>Ngẫu nhiên';
                    this.disabled = false;

                    // Add success animation
                    this.style.background = '#28a745';
                    setTimeout(() => this.style.background = '', 2000);
                }, 800);
            }
        });
    }

    if (firstBtn) {
        firstBtn.addEventListener('click', function () {
            const firstOption = userIdSelect.querySelector('option[value!=""]');
            if (firstOption) {
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang chọn...';
                this.disabled = true;

                setTimeout(() => {
                    userIdSelect.value = firstOption.value;
                    updateEnhancedCustomerInfo(firstOption.value, firstOption.textContent);
                    showModernToast('👤 Đã chọn khách hàng đầu tiên!', 'info');

                    this.innerHTML = '<i class="fas fa-user me-1"></i>Khách đầu tiên';
                    this.disabled = false;

                    this.style.background = '#17a2b8';
                    setTimeout(() => this.style.background = '', 2000);
                }, 600);
            }
        });
    }

    if (vipBtn) {
        vipBtn.addEventListener('click', function () {
            const options = userIdSelect.querySelectorAll('option[value!=""]');
            if (options.length > 0) {
                // Select from upper tier customers (simulating VIP)
                const vipIndex = Math.floor(options.length * 0.7 + Math.random() * options.length * 0.3);
                const vipOption = options[vipIndex];

                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Chọn VIP...';
                this.disabled = true;

                setTimeout(() => {
                    userIdSelect.value = vipOption.value;
                    updateEnhancedCustomerInfo(vipOption.value, vipOption.textContent + ' 👑');
                    showModernToast('👑 Đã chọn khách hàng VIP!', 'warning');

                    this.innerHTML = '<i class="fas fa-crown me-1"></i>VIP';
                    this.disabled = false;

                    this.style.background = '#ffc107';
                    this.style.color = '#212529';
                    setTimeout(() => {
                        this.style.background = '';
                        this.style.color = '';
                    }, 2000);
                }, 1000);
            }
        });
    }

    // Enhanced direct select change
    if (userIdSelect) {
        userIdSelect.addEventListener('change', function () {
            if (this.value) {
                const selectedOption = this.options[this.selectedIndex];
                updateEnhancedCustomerInfo(this.value, selectedOption.textContent);

                // Add visual feedback to select
                this.style.borderColor = '#28a745';
                setTimeout(() => this.style.borderColor = '', 2000);
            } else {
                updateEnhancedCustomerInfo('', '');
            }
        });

        // Add focus effects
        userIdSelect.addEventListener('focus', function () {
            this.parentElement.classList.add('select-focused');
        });

        userIdSelect.addEventListener('blur', function () {
            this.parentElement.classList.remove('select-focused');
        });
    }

    console.log('Modern customer selection initialized successfully!');
}

// Enhanced customer info display
function updateEnhancedCustomerInfo(customerId, customerText) {
    const customerInfo = document.getElementById('customerInfo');
    if (customerInfo) {
        if (customerId) {
            customerInfo.innerHTML = `
                <div class="customer-info-content">
                    <div class="customer-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="customer-details">
                        <div class="customer-name">${customerText}</div>
                        <div class="customer-id">ID: ${customerId}</div>
                        <div class="customer-status">
                            <span class="status-badge active">Hoạt động</span>
                        </div>
                    </div>
                    <div class="customer-actions">
                        <button class="btn btn-sm btn-outline-primary view-history">
                            <i class="fas fa-history me-1"></i>Lịch sử
                        </button>
                    </div>
                </div>
            `;

            // Add success animation
            customerInfo.style.transform = 'scale(1.02)';
            setTimeout(() => customerInfo.style.transform = 'scale(1)', 300);

        } else {
            customerInfo.innerHTML = `
                <div class="customer-info-placeholder">
                    <i class="fas fa-user-plus me-2"></i>
                    <span>Chọn khách hàng để xem thông tin</span>
                </div>
            `;
        }
    }
}

// Highlight search item
function highlightSearchItem(items, index) {
    items.forEach(item => item.classList.remove('highlighted'));
    if (items[index]) {
        items[index].classList.add('highlighted');
        items[index].scrollIntoView({ block: 'nearest' });
    }
}

// Modern toast notification system
function showModernToast(message, type = 'info', duration = 4000) {
    // Remove existing toast
    const existingToast = document.querySelector('.modern-toast');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = `modern-toast toast-${type}`;

    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-crown',
        info: 'fas fa-info-circle'
    };

    const colors = {
        success: 'linear-gradient(135deg, #28a745, #20c997)',
        error: 'linear-gradient(135deg, #dc3545, #fd7e14)',
        warning: 'linear-gradient(135deg, #ffc107, #fd7e14)',
        info: 'linear-gradient(135deg, #17a2b8, #6f42c1)'
    };

    toast.innerHTML = `
        <div class="toast-icon">
            <i class="${icons[type] || icons.info}"></i>
        </div>
        <div class="toast-content">
            <div class="toast-message">${message}</div>
            <div class="toast-progress"></div>
        </div>
        <button class="toast-close" onclick="this.closest('.modern-toast').remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    toast.style.background = colors[type] || colors.info;

    document.body.appendChild(toast);

    // Auto remove with animation
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.4s ease';
        setTimeout(() => toast.remove(), 400);
    }, duration);

    return toast;
}

// Modern UI initialization
function initModernUI() {
    // Add modern CSS if not exists
    if (!document.getElementById('modernUIStyles')) {
        const style = document.createElement('style');
        style.id = 'modernUIStyles';
        style.textContent = `
            /* Modern Toast Notifications */
            .modern-toast {
                position: fixed;
                top: 20px;
                right: 20px;
                min-width: 320px;
                max-width: 500px;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                z-index: 10000;
                animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                overflow: hidden;
                backdrop-filter: blur(10px);
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1.5rem;
                color: white;
                font-weight: 500;
            }
            
            .toast-icon {
                font-size: 1.5rem;
                opacity: 0.9;
            }
            
            .toast-content {
                flex: 1;
                position: relative;
            }
            
            .toast-message {
                font-size: 0.95rem;
                line-height: 1.4;
                margin-bottom: 0.75rem;
            }
            
            .toast-progress {
                height: 3px;
                background: rgba(255,255,255,0.3);
                border-radius: 2px;
                animation: progressBar 4s linear;
                transform-origin: left;
            }
            
            .toast-close {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
            }
            
            .toast-close:hover {
                background: rgba(255,255,255,0.3);
                transform: scale(1.1);
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideOutRight {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(100%);
                }
            }
            
            @keyframes progressBar {
                from { transform: scaleX(1); }
                to { transform: scaleX(0); }
            }
            
            /* Enhanced Customer Info */
            .customer-info-content {
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1rem;
            }
            
            .customer-avatar {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.2rem;
            }
            
            .customer-details {
                flex: 1;
            }
            
            .customer-name {
                font-weight: 600;
                font-size: 1rem;
                color: #333;
                margin-bottom: 0.25rem;
            }
            
            .customer-id {
                font-size: 0.85rem;
                color: #6c757d;
                margin-bottom: 0.5rem;
            }
            
            .status-badge {
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .status-badge.active {
                background: #d4edda;
                color: #155724;
            }
            
            .customer-info-placeholder {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                color: #6c757d;
                font-style: italic;
            }
            
            /* Enhanced Search Results */
            .search-result-item {
                display: flex;
                align-items: center;
                padding: 0.75rem 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                border-bottom: 1px solid #f8f9fa;
                animation: fadeInUp 0.3s ease;
            }
            
            .search-result-item:hover {
                background: #f8f9fa;
                transform: translateX(5px);
            }
            
            .search-result-item.highlighted {
                background: #e3f2fd;
                border-left: 3px solid #2196f3;
            }
            
            .search-result-item.no-results {
                color: #6c757d;
                cursor: default;
            }
            
            .search-result-item.no-results:hover {
                background: none;
                transform: none;
            }
            
            .result-text {
                flex: 1;
                margin: 0 0.5rem;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Enhanced Select Focus */
            .select-focused {
                transform: scale(1.02);
                transition: transform 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }
}

// Particles effect for hero section
function createParticlesEffect() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    const canvas = document.createElement('canvas');
    canvas.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    `;

    heroSection.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let particles = [];

    function resizeCanvas() {
        canvas.width = heroSection.offsetWidth;
        canvas.height = heroSection.offsetHeight;
    }

    function createParticle() {
        return {
            x: Math.random() * canvas.width,
            y: canvas.height + 10,
            size: Math.random() * 4 + 2,
            speed: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.2,
            color: `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2})`
        };
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((particle, index) => {
            particle.y -= particle.speed;
            particle.opacity -= 0.002;

            if (particle.opacity <= 0 || particle.y < -10) {
                particles.splice(index, 1);
            }

            ctx.globalAlpha = particle.opacity;
            ctx.fillStyle = particle.color;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
        });

        if (Math.random() < 0.3) {
            particles.push(createParticle());
        }

        requestAnimationFrame(animateParticles);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    animateParticles();
}

// Enhanced form handling
function initEnhancedFormHandling() {
    const form = document.getElementById('recommendationForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const userId = document.getElementById('userId').value;
        const type = document.getElementById('recommendationType').value;

        if (!userId) {
            showCustomerSelectionHelper();
            showModernToast('⚠️ Vui lòng chọn khách hàng trước!', 'warning');
            return;
        }

        if (!type) {
            showModernToast('⚠️ Vui lòng chọn loại gợi ý!', 'warning');
            return;
        }

        // Show loading state
        showModernToast('🔄 Đang tải gợi ý món ăn...', 'info', 6000);

        // Proceed with form submission
        handleFormSubmission(userId, type);
    });
}

// Show customer selection helper
function showCustomerSelectionHelper() {
    const userIdSelect = document.getElementById('userId');
    const wrapper = userIdSelect.closest('.customer-select-wrapper');

    userIdSelect.classList.add('is-invalid');
    userIdSelect.focus();

    // Scroll to customer selection
    wrapper.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Add helper animation
    wrapper.style.animation = 'shake 0.5s ease';
    setTimeout(() => wrapper.style.animation = '', 500);

    // Add shake animation if not exists
    if (!document.getElementById('shakeAnimation')) {
        const style = document.createElement('style');
        style.id = 'shakeAnimation';
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }

    // Remove invalid state after selection
    userIdSelect.addEventListener('change', function () {
        this.classList.remove('is-invalid');
    }, { once: true });
}

// Placeholder for other functions
function initDarkMode() {
    // Dark mode toggle functionality
    console.log('Dark mode initialized');
}

function initSmoothTransitions() {
    // Smooth transition effects
    console.log('Smooth transitions initialized');
}

function initFormValidation() {
    // Form validation
    console.log('Form validation initialized');
}

function initModernNavbar() {
    // Modern navbar functionality
    console.log('Modern navbar initialized');
}

function handleFormSubmission(userId, type) {
    // Handle form submission
    console.log('Form submitted:', userId, type);
}

console.log('🎉 Modern Vietnamese Food Recommendation System loaded successfully!');
