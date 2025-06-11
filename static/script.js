// Modern Vietnamese Food Recommendation System - Enhanced UI
// Author: AI Assistant
// Version: 2.0

// Ensure no conflicts and proper initialization
(function () {
    'use strict';

    console.log('🚀 Loading enhanced Vietnamese Food Recommendation System...');

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeSystem);
    } else {
        initializeSystem();
    }

    function initializeSystem() {
        console.log('🎯 Initializing system...');

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

            // Initialize navbar and navigation
            initModernNavbar();

            // Initialize form handling - This is crucial!
            setTimeout(() => {
                initEnhancedFormHandling();
                console.log('✅ Enhanced form handling initialized');
            }, 800);

            // Initialize recommendation type handler
            initRecommendationTypeHandler();

            // Initialize particles effect
            createParticlesEffect();            // Initialize nutrition recommendations and meal plans
            setTimeout(() => {
                try {
                    initNutritionRecommendations();
                    initMealPlans();
                    console.log('✅ Nutrition and meal plans initialized');

                    // Thêm event listener bổ sung để đảm bảo auto-load
                    setTimeout(() => {
                        setupAutoLoadListener();
                    }, 1000);

                    // Show initial placeholders
                    const nutritionContainer = document.getElementById('nutrition-recommendations');
                    const mealPlansContainer = document.getElementById('meal-plans-content');

                    if (nutritionContainer && !nutritionContainer.innerHTML.trim()) {
                        nutritionContainer.innerHTML = `
                            <div class="nutrition-placeholder">
                                <div class="placeholder-icon">
                                    <i class="fas fa-user-plus fa-3x"></i>
                                </div>
                                <div class="placeholder-content">
                                    <h4>Chọn khách hàng để xem gợi ý dinh dưỡng</h4>
                                    <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem các gợi ý dinh dưỡng phù hợp</p>
                                </div>
                            </div>
                        `;
                    }

                    if (mealPlansContainer && !mealPlansContainer.innerHTML.trim()) {
                        mealPlansContainer.innerHTML = `
                            <div class="meal-plans-placeholder">
                                <div class="placeholder-icon">
                                    <i class="fas fa-user-plus fa-3x"></i>
                                </div>
                                <div class="placeholder-content">
                                    <h4>Chọn khách hàng để xem thực đơn gợi ý</h4>
                                    <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem thực đơn theo bữa phù hợp</p>
                                </div>
                            </div>
                        `;
                    }

                } catch (error) {
                    console.error('❌ Error initializing nutrition/meal plans:', error);
                }
            }, 1500);

            // Show welcome message
            setTimeout(() => {
                if (typeof showModernToast === 'function') {
                    showModernToast('🍽️ Chào mừng đến với hệ thống gợi ý món ăn!', 'success', 4000);
                }
            }, 2000);

            console.log('✅ All systems initialized successfully');

        } catch (error) {
            console.error('❌ System initialization error:', error);
        }
    }
})();

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
                    this.style.color = 'white'; setTimeout(() => {
                        userIdSelect.value = value;
                        updateEnhancedCustomerInfo(value, text);
                        searchInput.value = '';
                        searchResults.innerHTML = '';
                        searchBox.classList.remove('active');
                        toggleSearchBtn.innerHTML = '<i class="fas fa-search me-1"></i>Tìm kiếm';
                        showModernToast('✅ Đã chọn: ' + text, 'success');

                        // Auto-reload nutrition and meal plans
                        setTimeout(() => reloadNutritionAndMealPlans(), 300);
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
                this.disabled = true; setTimeout(() => {
                    userIdSelect.value = randomOption.value;
                    updateEnhancedCustomerInfo(randomOption.value, randomOption.textContent);
                    showModernToast('🎲 Đã chọn khách hàng ngẫu nhiên!', 'success');

                    // Reset button
                    this.innerHTML = '<i class="fas fa-random me-1"></i>Ngẫu nhiên';
                    this.disabled = false;

                    // Add success animation
                    this.style.background = '#28a745';
                    setTimeout(() => this.style.background = '', 2000);

                    // Auto-reload nutrition and meal plans
                    setTimeout(() => reloadNutritionAndMealPlans(), 300);
                }, 800);
            }
        });
    }

    if (firstBtn) {
        firstBtn.addEventListener('click', function () {
            const firstOption = userIdSelect.querySelector('option[value!=""]');
            if (firstOption) {
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang chọn...';
                this.disabled = true; setTimeout(() => {
                    userIdSelect.value = firstOption.value;
                    updateEnhancedCustomerInfo(firstOption.value, firstOption.textContent);
                    showModernToast('👤 Đã chọn khách hàng đầu tiên!', 'info');

                    this.innerHTML = '<i class="fas fa-user me-1"></i>Khách đầu tiên';
                    this.disabled = false;

                    this.style.background = '#17a2b8';
                    setTimeout(() => this.style.background = '', 2000);

                    // Auto-reload nutrition and meal plans
                    setTimeout(() => reloadNutritionAndMealPlans(), 300);
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
                this.disabled = true; setTimeout(() => {
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

                    // Auto-reload nutrition and meal plans
                    setTimeout(() => reloadNutritionAndMealPlans(), 300);
                }, 1000);
            }
        });
    }    // Enhanced direct select change
    if (userIdSelect) {
        userIdSelect.addEventListener('change', function () {
            console.log('🔄 Customer selection changed, value:', this.value);
            console.log('🔄 Customer selection changed, selected text:', this.options[this.selectedIndex]?.textContent);

            if (this.value) {
                const selectedOption = this.options[this.selectedIndex];
                console.log('Selected option:', selectedOption.textContent);

                updateEnhancedCustomerInfo(this.value, selectedOption.textContent);                // Add visual feedback to select
                this.style.borderColor = '#28a745';
                setTimeout(() => this.style.borderColor = '', 2000);

                // NGAY LẬP TỨC hiển thị loading và tự động tải cả 2 phần
                console.log('🚀 BẮTĐẦU tự động tải ngay lập tức cho:', this.value);

                // Hiển thị loading indicators ngay lập tức
                const nutritionContainer = document.getElementById('nutrition-recommendations');
                const mealPlansContainer = document.getElementById('meal-plans-content');

                if (nutritionContainer) {
                    nutritionContainer.innerHTML = `
                        <div class="text-center py-5">
                            <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <h4 class="text-primary">🥗 Đang tải gợi ý dinh dưỡng...</h4>
                            <p class="text-muted">Khách hàng: ${selectedOption.textContent}</p>
                        </div>
                    `;
                }

                if (mealPlansContainer) {
                    mealPlansContainer.innerHTML = `
                        <div class="text-center py-5">
                            <div class="spinner-border text-success mb-3" role="status" style="width: 3rem; height: 3rem;">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <h4 class="text-success">🍽️ Đang tải thực đơn theo bữa...</h4>
                            <p class="text-muted">Khách hàng: ${selectedOption.textContent}</p>
                        </div>
                    `;
                }

                // Toast thông báo
                if (typeof showModernToast === 'function') {
                    showModernToast(`🔄 Tự động tải gợi ý cho ${selectedOption.textContent}...`, 'info', 3000);
                }                // Gọi hàm reload ngay lập tức
                console.log('⏳ Gọi reloadNutritionAndMealPlans() ngay lập tức');
                setTimeout(async () => {
                    await reloadNutritionAndMealPlans();
                }, 100); // Giảm delay xuống chỉ 100ms
            } else {
                console.log('❌ No customer selected, clearing info');
                updateEnhancedCustomerInfo('', '');

                // Clear nutrition and meal plans sections
                const nutritionContainer = document.getElementById('nutrition-recommendations');
                const mealPlansContainer = document.getElementById('meal-plans-content');

                if (nutritionContainer) {
                    nutritionContainer.innerHTML = `
                        <div class="nutrition-placeholder">
                            <div class="placeholder-icon">
                                <i class="fas fa-user-plus fa-3x"></i>
                            </div>
                            <div class="placeholder-content">
                                <h4>Chọn khách hàng để xem gợi ý dinh dưỡng</h4>
                                <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem các gợi ý dinh dưỡng phù hợp</p>
                            </div>
                        </div>
                    `;
                }

                if (mealPlansContainer) {
                    mealPlansContainer.innerHTML = `
                        <div class="meal-plans-placeholder">
                            <div class="placeholder-icon">
                                <i class="fas fa-user-plus fa-3x"></i>
                            </div>
                            <div class="placeholder-content">
                                <h4>Chọn khách hàng để xem thực đơn gợi ý</h4>
                                <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem thực đơn theo bữa phù hợp</p>
                            </div>
                        </div>
                    `;
                }
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
    if (!form) {
        console.error('❌ Form not found: recommendationForm');
        return;
    }

    console.log('✅ Form found, adding submit event listener');

    // Remove any existing event listeners first
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);

    // Add fresh event listener
    newForm.addEventListener('submit', function (e) {
        e.preventDefault();
        e.stopPropagation();

        console.log('🚀 Form submit event triggered');

        const userId = document.getElementById('userId').value;
        const type = document.getElementById('recommendationType').value;

        console.log('Form values:', { userId, type });

        // Validate userId
        if (!userId || userId.trim() === '') {
            console.log('❌ No userId selected');
            const userIdSelect = document.getElementById('userId');
            userIdSelect.classList.add('is-invalid');
            userIdSelect.focus();

            if (typeof showModernToast === 'function') {
                showModernToast('⚠️ Vui lòng chọn khách hàng trước!', 'warning');
            } else {
                alert('Vui lòng chọn khách hàng trước!');
            }
            return false;
        }

        // Validate type
        if (!type || type.trim() === '') {
            console.log('❌ No recommendation type selected');
            const typeSelect = document.getElementById('recommendationType');
            typeSelect.classList.add('is-invalid');
            typeSelect.focus();

            if (typeof showModernToast === 'function') {
                showModernToast('⚠️ Vui lòng chọn loại gợi ý!', 'warning');
            } else {
                alert('Vui lòng chọn loại gợi ý!');
            }
            return false;
        }

        // Clear invalid states
        document.getElementById('userId').classList.remove('is-invalid');
        document.getElementById('recommendationType').classList.remove('is-invalid');

        // Show loading state
        console.log('✅ Validation passed, showing loading toast');
        if (typeof showModernToast === 'function') {
            showModernToast('🔄 Đang tải gợi ý món ăn...', 'info', 6000);
        }

        // Proceed with form submission
        console.log('✅ Calling handleFormSubmission');
        try {
            handleFormSubmission(userId, type);
        } catch (error) {
            console.error('❌ Error in handleFormSubmission:', error);
            if (typeof showModernToast === 'function') {
                showModernToast('❌ Có lỗi xảy ra: ' + error.message, 'error');
            } else {
                alert('Có lỗi xảy ra: ' + error.message);
            }
        }

        return false; // Prevent any default form submission
    });

    console.log('✅ Enhanced form handling initialized');
}

// Initialize recommendation type change handler
function initRecommendationTypeHandler() {
    const recommendationType = document.getElementById('recommendationType');
    const itemIdOption = document.getElementById('itemIdOption');
    const mainDishIdOption = document.getElementById('mainDishIdOption');
    const familySizeOption = document.getElementById('familySizeOption');
    const ageGroupOption = document.getElementById('ageGroupOption');

    if (!recommendationType) return;

    const allOptions = [itemIdOption, mainDishIdOption, familySizeOption, ageGroupOption];

    recommendationType.addEventListener('change', function () {
        // Hide all options first with fade out
        allOptions.forEach(option => {
            if (option && !option.classList.contains('d-none')) {
                option.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    option.classList.add('d-none');
                    option.style.animation = '';
                }, 300);
            }
        });

        // Show relevant options based on selection with fade in
        setTimeout(() => {
            switch (this.value) {
                case 'upsell_combos':
                    if (itemIdOption) showOptionWithAnimation(itemIdOption);
                    break;
                case 'upsell_sides':
                    if (mainDishIdOption) showOptionWithAnimation(mainDishIdOption);
                    break;
                case 'family_combos':
                    if (familySizeOption) showOptionWithAnimation(familySizeOption);
                    break;
                case 'age_based':
                    if (ageGroupOption) showOptionWithAnimation(ageGroupOption);
                    break;
            }
        }, 150);
    });

    // Helper function to show options with animation
    function showOptionWithAnimation(option) {
        option.classList.remove('d-none');
        option.style.animation = 'fadeIn 0.5s ease';
        setTimeout(() => {
            option.style.animation = '';
        }, 500);
    }
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

// Initialize nutrition recommendations
function initNutritionRecommendations() {
    console.log('Initializing nutrition recommendations...');

    // Add event listeners for nutrition navigation buttons
    const nutritionNavItems = document.querySelectorAll('.nutrition-nav-item');
    nutritionNavItems.forEach(item => {
        item.addEventListener('click', function () {
            // Remove active class from all items
            nutritionNavItems.forEach(navItem => navItem.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');

            // Load recommendations for selected nutrition type
            const nutritionType = this.getAttribute('data-nutrition');
            loadNutritionRecommendations(nutritionType);
        });
    });

    // Don't load default recommendations - wait for customer selection
    console.log('✅ Nutrition navigation initialized, waiting for customer selection');
}

// Initialize meal plans
function initMealPlans() {
    console.log('Initializing meal plans...');

    // Don't load default meal plans - wait for customer selection
    console.log('✅ Meal plans initialized, waiting for customer selection');
}

// Setup backup auto-load listener to ensure it works
function setupAutoLoadListener() {
    console.log('🔧 Setting up backup auto-load listener...');

    const userIdSelect = document.getElementById('userId');
    if (!userIdSelect) {
        console.log('❌ User ID select not found for backup listener');
        return;
    }

    // Remove existing event listeners to avoid duplicates
    const newSelect = userIdSelect.cloneNode(true);
    userIdSelect.parentNode.replaceChild(newSelect, userIdSelect);

    // Add fresh event listener
    newSelect.addEventListener('change', async function () {
        console.log('🔄 BACKUP: Customer selection changed, value:', this.value);

        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            console.log('🔄 BACKUP: Selected customer:', selectedOption.textContent);

            // Show immediate loading feedback
            const nutritionContainer = document.getElementById('nutrition-recommendations');
            const mealPlansContainer = document.getElementById('meal-plans-content');

            if (nutritionContainer) {
                nutritionContainer.innerHTML = `
                    <div class="text-center py-5">
                        <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h4 class="text-primary">🥗 Đang tải gợi ý dinh dưỡng...</h4>
                        <p class="text-muted">Khách hàng: ${selectedOption.textContent}</p>
                    </div>
                `;
            }

            if (mealPlansContainer) {
                mealPlansContainer.innerHTML = `
                    <div class="text-center py-5">
                        <div class="spinner-border text-success mb-3" role="status" style="width: 3rem; height: 3rem;">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h4 class="text-success">🍽️ Đang tải thực đơn theo bữa...</h4>
                        <p class="text-muted">Khách hàng: ${selectedOption.textContent}</p>
                    </div>
                `;
            }

            // Force reload with delay
            setTimeout(async () => {
                console.log('🚀 BACKUP: Force loading both sections...');
                await reloadNutritionAndMealPlans();
            }, 200);
        }
    });

    console.log('✅ Backup auto-load listener setup completed');
}

// Auto-reload nutrition and meal plans when customer changes
async function reloadNutritionAndMealPlans() {
    console.log('🔄 === BẮT BUỘC RELOAD NUTRITION AND MEAL PLANS ===');

    const activeNutritionItem = document.querySelector('.nutrition-nav-item.active');
    const nutritionType = activeNutritionItem ? activeNutritionItem.getAttribute('data-nutrition') : 'weight-loss';

    console.log('🥗 Selected nutrition type:', nutritionType);
    console.log('🥗 Active nutrition item found:', !!activeNutritionItem);

    // Check if containers exist
    const nutritionContainer = document.getElementById('nutrition-recommendations');
    const mealPlansContainer = document.getElementById('meal-plans-content');

    console.log('📦 Nutrition container found:', !!nutritionContainer);
    console.log('📦 Meal plans container found:', !!mealPlansContainer);

    // Check customer ID
    const userIdElement = document.getElementById('userId');
    const userId = userIdElement?.value;
    console.log('👤 Current user ID:', userId);

    if (!userId) {
        console.log('❌ No user ID, cannot load recommendations');
        return;
    }

    // BẮT BUỘC tải cả 2 phần song song
    console.log('🔄 === BẮT BUỘC LOADING BOTH SECTIONS SIMULTANEOUSLY ===');

    const promises = [];

    if (nutritionContainer) {
        console.log('🔄 === STARTING NUTRITION RECOMMENDATIONS ===');
        promises.push(
            loadNutritionRecommendations(nutritionType)
                .then(() => console.log('✅ Nutrition recommendations loading COMPLETED'))
                .catch(error => console.error('❌ Error loading nutrition recommendations:', error))
        );
    }

    if (mealPlansContainer) {
        console.log('🔄 === STARTING MEAL PLANS ===');
        promises.push(
            loadMealPlans()
                .then(() => console.log('✅ Meal plans loading COMPLETED'))
                .catch(error => console.error('❌ Error loading meal plans:', error))
        );
    }

    // Wait for both to complete
    try {
        await Promise.all(promises);
        console.log('🔄 === ALL FORCED RELOAD COMPLETED ===');
    } catch (error) {
        console.error('❌ Error in parallel loading:', error);
    }
}

// Scroll to nutrition section
function scrollToNutrition() {
    const nutritionSection = document.getElementById('nutrition');
    if (nutritionSection) {
        nutritionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Scroll to meal plans section
function scrollToMealPlans() {
    const mealPlansSection = document.getElementById('meal-plans');
    if (mealPlansSection) {
        mealPlansSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Placeholder for other functions
function initDarkMode() {
    // Dark mode toggle functionality
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Load saved preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }
    console.log('Dark mode initialized');
}

function initSmoothTransitions() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add transition classes to form elements
    const formElements = document.querySelectorAll('.form-control, .form-select, .btn');
    formElements.forEach(element => {
        element.style.transition = 'all 0.3s ease';
    });

    console.log('Smooth transitions initialized');
}

function initFormValidation() {
    // Add real-time validation
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function () {
            if (!this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });

        field.addEventListener('input', function () {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

    console.log('Form validation initialized');
}

function initModernNavbar() {
    // Navbar scroll effect
    window.addEventListener('scroll', function () {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        }
    });

    // Mobile menu auto-close
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                navbarToggler?.click();
            }
        });
    });

    console.log('Modern navbar initialized');
}

function handleFormSubmission(userId, type) {
    console.log('🚀 Submitting form:', { userId, type });

    // Get results container
    const resultsContainer = document.getElementById('recommendationResults');
    if (!resultsContainer) {
        console.error('Results container not found!');
        return;
    }

    // Show loading skeleton
    showLoadingSkeleton(resultsContainer);

    // Scroll to results section
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Prepare API URL and parameters
    let apiUrl = '/api/';
    let params = new URLSearchParams();
    params.append('user_id', userId);

    // Get additional parameters based on recommendation type
    switch (type) {
        case 'upsell_combos':
            apiUrl += 'upsell_combos';
            const itemId = document.getElementById('itemId')?.value || '54';
            params.append('item_id', itemId);
            break;
        case 'upsell_sides':
            apiUrl += 'upsell_sides';
            const mainDishId = document.getElementById('mainDishId')?.value || '54';
            params.append('main_dish_id', mainDishId);
            break;
        case 'family_combos':
            apiUrl += 'family_combos';
            const familySize = document.getElementById('familySize')?.value || '4';
            params.append('family_size', familySize);
            break;
        case 'age_based':
            apiUrl += 'age_based_recommendations';
            const ageGroup = document.getElementById('ageGroup')?.value || 'adults';
            params.append('age_group', ageGroup);
            break;
        default:
            showModernToast('❌ Loại gợi ý không hợp lệ!', 'error');
            return;
    }

    // Make API request
    fetch(`${apiUrl}?${params.toString()}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('✅ API Response:', data);
            displayRecommendationResults(data, type);
            showModernToast('🎉 Gợi ý món ăn đã được tải thành công!', 'success');
        })
        .catch(error => {
            console.error('❌ API Error:', error);
            showErrorMessage(resultsContainer, error.message);
            showModernToast('❌ Có lỗi xảy ra khi tải gợi ý!', 'error');
        });
}

// Display recommendation results based on type
function displayRecommendationResults(data, type) {
    const resultsContainer = document.getElementById('recommendationResults');

    let html = '';

    switch (type) {
        case 'upsell_combos':
            html = generateComboResults(data);
            break;
        case 'upsell_sides':
            html = generateSidesResults(data);
            break;
        case 'family_combos':
            html = generateFamilyResults(data);
            break;
        case 'age_based':
            html = generateAgeBasedResults(data);
            break;
    }

    // Add fade-in animation
    resultsContainer.style.opacity = '0';
    resultsContainer.innerHTML = html;

    setTimeout(() => {
        resultsContainer.style.transition = 'opacity 0.5s ease';
        resultsContainer.style.opacity = '1';
    }, 100);
}

// Missing helper functions
function showLoadingSkeleton(container) {
    const skeletonHTML = `
        <div class="loading-skeleton">
            <div class="skeleton-header">
                <div class="skeleton-title"></div>
                <div class="skeleton-subtitle"></div>
            </div>
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="skeleton-card">
                        <div class="skeleton-image"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                            <div class="skeleton-rating"></div>
                            <div class="skeleton-buttons"></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="skeleton-card">
                        <div class="skeleton-image"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                            <div class="skeleton-rating"></div>
                            <div class="skeleton-buttons"></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="skeleton-card">
                        <div class="skeleton-image"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                            <div class="skeleton-rating"></div>
                            <div class="skeleton-buttons"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.innerHTML = skeletonHTML;
}

function showErrorMessage(container, message) {
    container.innerHTML = `
        <div class="error-message">
            <div class="error-icon">
                <i class="fas fa-exclamation-triangle fa-3x text-warning"></i>
            </div>
            <h4 class="mt-3">Có lỗi xảy ra</h4>
            <p class="text-muted">${message}</p>
            <button class="btn btn-primary" onclick="location.reload()">
                <i class="fas fa-refresh me-2"></i>Thử lại
            </button>
        </div>
    `;
}

// Utility functions
function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    let starsHtml = '';

    for (let i = 0; i < fullStars; i++) {
        starsHtml += '<i class="fas fa-star text-warning"></i>';
    }

    if (halfStar) {
        starsHtml += '<i class="fas fa-star-half-alt text-warning"></i>';
    }

    for (let i = 0; i < emptyStars; i++) {
        starsHtml += '<i class="far fa-star text-warning"></i>';
    }

    return starsHtml;
}

function getDifficultyClass(difficulty) {
    switch (difficulty) {
        case 'Dễ':
            return 'difficulty-easy';
        case 'Trung bình':
            return 'difficulty-medium';
        case 'Khó':
            return 'difficulty-hard';
        default:
            return 'difficulty-medium';
    }
}

function getMealTimeClass(mealTime) {
    switch (mealTime) {
        case 'breakfast':
        case 'sáng':
            return 'meal-time-breakfast';
        case 'lunch':
        case 'trưa':
            return 'meal-time-lunch';
        case 'dinner':
        case 'tối':
            return 'meal-time-dinner';
        default:
            return 'meal-time-general';
    }
}

function translateMealTime(mealTime) {
    switch (mealTime) {
        case 'breakfast':
            return 'Sáng';
        case 'lunch':
            return 'Trưa';
        case 'dinner':
            return 'Tối';
        case 'sáng':
            return 'Sáng';
        case 'trưa':
            return 'Trưa';
        case 'tối':
            return 'Tối';
        default:
            return 'Cả ngày';
    }
}

function translateAgeGroup(ageGroup) {
    switch (ageGroup) {
        case 'children':
            return 'Trẻ em (3-12 tuổi)';
        case 'teenagers':
            return 'Thanh thiếu niên (13-19 tuổi)';
        case 'adults':
            return 'Người lớn (20-59 tuổi)';
        case 'elderly':
            return 'Người cao tuổi (60+ tuổi)';
        default:
            return 'Tất cả độ tuổi';
    }
}

function translateNutritionType(nutritionType) {
    switch (nutritionType) {
        case 'weight-loss':
            return 'Giảm cân';
        case 'balanced':
            return 'Cân bằng dinh dưỡng';
        case 'blood-boost':
            return 'Bổ máu';
        case 'brain-boost':
            return 'Tăng cường trí não';
        case 'digestive-support':
            return 'Hỗ trợ tiêu hóa'; default:
            return 'Dinh dưỡng cơ bản';
    }
}

// Price formatting utility function
function formatPrice(price) {
    if (typeof price !== 'number') {
        price = parseFloat(price) || 0;
    }
    return price.toLocaleString('vi-VN');
}

// Helper functions for loading skeletons
function showNutritionLoadingSkeleton(container) {
    container.innerHTML = `
        <div class="nutrition-loading-skeleton">
            ${Array(6).fill().map(() => `
                <div class="skeleton-card">
                    <div class="skeleton-image"></div>
                    <div class="skeleton-content">
                        <div class="skeleton-line"></div>
                        <div class="skeleton-line short"></div>
                        <div class="skeleton-rating"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function showMealPlansLoadingSkeleton(container) {
    container.innerHTML = `
        <div class="meal-plans-skeleton">
            ${Array(3).fill().map(() => `
                <div class="skeleton-menu-column">
                    <div class="skeleton-header"></div>
                    <div class="skeleton-meal"></div>
                    <div class="skeleton-meal"></div>
                    <div class="skeleton-meal"></div>
                    <div class="skeleton-button"></div>
                </div>
            `).join('')}
        </div>
    `;
}

function showNutritionError(container, message) {
    container.innerHTML = `
        <div class="nutrition-error">
            <div class="error-icon">
                <i class="fas fa-exclamation-triangle fa-2x text-warning"></i>
            </div>
            <h5 class="mt-3">Không thể tải gợi ý dinh dưỡng</h5>
            <p class="text-muted">${message}</p>
            <button class="btn btn-outline-primary" onclick="location.reload()">
                <i class="fas fa-refresh me-2"></i>Thử lại
            </button>
        </div>
    `;
}

function showMealPlansError(container, message) {
    container.innerHTML = `
        <div class="meal-plans-error">
            <div class="error-icon">
                <i class="fas fa-exclamation-triangle fa-2x text-warning"></i>
            </div>
            <h5 class="mt-3">Không thể tải thực đơn</h5>
            <p class="text-muted">${message}</p>
            <button class="btn btn-outline-primary" onclick="location.reload()">
                <i class="fas fa-refresh me-2"></i>Thử lại
            </button>
        </div>
    `;
}

// Generate combo results HTML
function generateComboResults(data) {
    return `
        <div class="col-12 mb-4">
            <div class="results-header">
                <h2 class="results-title">
                    <i class="fas fa-utensils me-3"></i>
                    ${data.message || 'Combo món ăn được gợi ý'}
                </h2>
                <p class="results-subtitle">Các combo món ăn phù hợp với sở thích của bạn</p>
            </div>
        </div>
        
        <div class="col-12">
            <div class="combo-promotion-box">
                <div class="promotion-header">
                    <i class="fas fa-star"></i>
                    <h3>Combo đặc biệt - Giảm giá 10%</h3>
                    <span class="promotion-badge">HOT</span>
                </div>
                <div class="row">
                    ${data.combo_recommendations?.map(item => `
                        <div class="col-lg-4 col-md-6 mb-4">
                            <div class="food-card combo-card">
                                <div class="food-image">
                                    <div class="image-placeholder">
                                        <i class="fas fa-utensils"></i>
                                        <span>Combo</span>
                                    </div>
                                    <div class="food-badge combo-badge">-10%</div>
                                </div>
                                <div class="food-content">
                                    <h5 class="food-title">${item.recipe_name}</h5>
                                    <div class="food-rating">
                                        ${generateStars(item.predicted_rating)}
                                        <span class="rating-value">${item.predicted_rating.toFixed(1)}</span>
                                    </div>
                                    <div class="food-price">
                                        <span class="original-price">${(parseFloat(item.combo_price.replace(/[^\d]/g, '')) * 1.1).toLocaleString()}đ</span>
                                        <span class="current-price">${item.combo_price}</span>
                                    </div>
                                    <div class="food-actions">
                                        <a href="${item.recipe_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                                            <i class="fas fa-book-open me-1"></i>Công thức
                                        </a>
                                        <button class="btn btn-success btn-sm">
                                            <i class="fas fa-cart-plus me-1"></i>Thêm vào giỏ
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('') || '<div class="col-12"><p class="text-center">Không có combo nào được tìm thấy.</p></div>'}
                </div>
                <div class="combo-actions">
                    <button class="btn btn-lg btn-gradient">
                        <i class="fas fa-shopping-cart me-2"></i>
                        Đặt tất cả combo này
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Generate sides results HTML
function generateSidesResults(data) {
    return `
        <div class="col-12 mb-4">
            <div class="results-header">
                <h2 class="results-title">
                    <i class="fas fa-leaf me-3"></i>
                    ${data.message || 'Món phụ được gợi ý'}
                </h2>
                <p class="results-subtitle">Những món phụ tuyệt vời để bổ sung cho bữa ăn</p>
            </div>
        </div>
        
        <div class="col-12">
            <div class="row">
                ${data.side_dish_recommendations?.map(item => `
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="food-card side-card">
                            <div class="food-image">
                                <div class="image-placeholder">
                                    <i class="fas fa-salad-bowl"></i>
                                    <span>Món phụ</span>
                                </div>
                            </div>
                            <div class="food-content">
                                <h5 class="food-title">${item.recipe_name}</h5>
                                <div class="food-rating">
                                    ${generateStars(item.predicted_rating)}
                                    <span class="rating-value">${item.predicted_rating.toFixed(1)}</span>
                                </div>
                                <div class="food-price">
                                    <span class="current-price">${item.side_price}</span>
                                </div>
                                <div class="food-actions">
                                    <a href="${item.recipe_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                                        <i class="fas fa-book-open me-1"></i>Công thức
                                    </a>
                                    <button class="btn btn-success btn-sm">
                                        <i class="fas fa-plus me-1"></i>Thêm món
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('') || '<div class="col-12"><p class="text-center">Không có món phụ nào được tìm thấy.</p></div>'}
            </div>
        </div>
    `;
}

// Generate family results HTML
function generateFamilyResults(data) {
    return `
        <div class="col-12 mb-4">
            <div class="results-header">
                <h2 class="results-title">
                    <i class="fas fa-users me-3"></i>
                    Combo gia đình đặc biệt
                </h2>
                <div class="family-info">
                    <span class="family-size">${data.suitable_for || 'Gia đình 4 người'}</span>
                    <span class="prep-time">
                        <i class="fas fa-clock me-1"></i>
                        ${data.preparation_time || '45 phút'}
                    </span>
                    <span class="total-price">
                        <i class="fas fa-tag me-1"></i>
                        ${data.total_price || 'Liên hệ'}
                    </span>
                </div>
            </div>
        </div>
        
        ${generateFamilySection('Món chính', data.family_combo?.main_dishes, 'main')}
        ${generateFamilySection('Món phụ', data.family_combo?.side_dishes, 'side')}
        ${generateFamilySection('Món tráng miệng', data.family_combo?.desserts, 'dessert')}
        
        <div class="col-12">
            <div class="family-combo-footer">
                <button class="btn btn-lg btn-gradient">
                    <i class="fas fa-heart me-2"></i>
                    Đặt combo gia đình này
                </button>
                <button class="btn btn-lg btn-outline-primary">
                    <i class="fas fa-share-alt me-2"></i>
                    Chia sẻ combo
                </button>
            </div>
        </div>
    `;
}

// Generate family section helper
function generateFamilySection(title, dishes, type) {
    if (!dishes || dishes.length === 0) return '';

    const icons = {
        main: 'fas fa-drumstick-bite',
        side: 'fas fa-leaf',
        dessert: 'fas fa-ice-cream'
    };

    return `
        <div class="col-12 mb-4">
            <div class="family-section">
                <h4 class="section-title">
                    <i class="${icons[type]} me-2"></i>
                    ${title}
                </h4>
                <div class="row">
                    ${dishes.map(dish => `
                        <div class="col-lg-4 col-md-6 mb-3">
                            <div class="food-card family-dish-card">
                                <div class="food-image">
                                    <div class="image-placeholder">
                                        <i class="${icons[type]}"></i>
                                        <span>${title}</span>
                                    </div>
                                </div>
                                <div class="food-content">
                                    <h6 class="food-title">${dish.recipe_name}</h6>
                                    <div class="food-meta">
                                        <span class="difficulty ${getDifficultyClass(dish.difficulty)}">
                                            ${dish.difficulty}
                                        </span>
                                    </div>
                                    <div class="food-rating">
                                        ${generateStars(dish.predicted_rating)}
                                        <span class="rating-value">${dish.predicted_rating.toFixed(1)}</span>
                                    </div>
                                    <a href="${dish.recipe_url}" target="_blank" class="btn btn-outline-primary btn-sm w-100">
                                        <i class="fas fa-book-open me-1"></i>Xem công thức
                                    </a>
                                </div>
                            </div>
                        </div>
                    `).join('')}

                </div>
            </div>
        </div>
    `;
}

// Generate age-based results HTML
function generateAgeBasedResults(data) {
    // Enhanced header with customer age info
    const customerAgeInfo = data.customer_age ?
        `<div class="customer-age-info">
            <i class="fas fa-user me-2"></i>
            <span>Khách hàng ${data.user_id} - ${data.customer_age} tuổi</span>
        </div>` : '';

    return `
        <div class="col-12 mb-4">
            <div class="results-header">
                <h2 class="results-title">
                    <i class="fas fa-birthday-cake me-3"></i>
                    Món ăn cho ${translateAgeGroup(data.age_group)}
                </h2>
                ${customerAgeInfo}
                <div class="nutrition-highlight">
                    <i class="fas fa-heart me-2"></i>
                    <span>${data.nutrition_focus || 'Dinh dưỡng cân bằng'}</span>
                </div>
                <div class="results-stats">
                    <span class="badge bg-primary me-2">
                        <i class="fas fa-utensils me-1"></i>
                        ${data.total_recommendations || data.recommendations?.length || 0} món
                    </span>
                    <span class="badge bg-success">
                        <i class="fas fa-thumbs-up me-1"></i>
                        Phù hợp ${translateAgeGroup(data.age_group)}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="col-12">
            <div class="row">
                ${data.recommendations?.map(item => `
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="food-card age-based-card">
                            <div class="food-image">
                                <div class="image-placeholder">
                                    <i class="fas fa-utensils"></i>
                                    <span>${translateAgeGroup(data.age_group)}</span>
                                </div>
                                <div class="meal-time-badge ${getMealTimeClass(item.meal_time)}">
                                    ${translateMealTime(item.meal_time)}
                                </div>
                            </div>
                            <div class="food-content">
                                <h5 class="food-title">${item.recipe_name}</h5>
                                <div class="food-meta">
                                    <span class="difficulty ${getDifficultyClass(item.difficulty)}">
                                        ${item.difficulty}
                                    </span>
                                    <span class="meal-time">
                                        ${translateMealTime(item.meal_time)}
                                    </span>
                                </div>
                                <div class="food-rating">
                                    ${generateStars(item.predicted_rating)}
                                    <span class="rating-value">${item.predicted_rating.toFixed(1)}</span>
                                </div>
                                ${item.estimated_calories || item.estimated_price_vnd ? `
                                <div class="food-details">
                                    ${item.estimated_calories ? `
                                        <small class="text-muted">
                                            <i class="fas fa-fire me-1"></i>${item.estimated_calories} cal
                                        </small>
                                    ` : ''}
                                    ${item.estimated_price_vnd ? `
                                        <small class="text-muted">
                                            <i class="fas fa-coins me-1"></i>${formatPrice(item.estimated_price_vnd)} VND
                                        </small>
                                    ` : ''}
                                </div>
                                ` : ''}
                                <div class="food-actions">
                                    <a href="${item.recipe_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                                        <i class="fas fa-book-open me-1"></i>Công thức
                                    </a>
                                    <button class="btn btn-success btn-sm">
                                        <i class="fas fa-plus me-1"></i>Thêm món
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('') || '<div class="col-12"><p class="text-center">Không có món ăn nào được tìm thấy.</p></div>'}
            </div>
        </div>
    `;
}

// Load nutrition recommendations
async function loadNutritionRecommendations(nutritionType = 'weight-loss') {
    console.log('🥗 === LOAD NUTRITION RECOMMENDATIONS STARTED ===');
    console.log('🥗 Loading nutrition recommendations, type:', nutritionType);

    const userIdElement = document.getElementById('userId');
    const userId = userIdElement?.value;
    const contentContainer = document.getElementById('nutrition-recommendations');

    console.log('🥗 User ID element found:', !!userIdElement);
    console.log('🥗 User ID value:', userId);
    console.log('🥗 Container found:', !!contentContainer);

    if (!contentContainer) {
        console.error('❌ Nutrition recommendations container not found!');
        return;
    }

    if (!userId || userId === '') {
        console.log('ℹ️ No user ID selected, showing placeholder');
        // Show friendly message instead of alert
        contentContainer.innerHTML = `
            <div class="nutrition-placeholder">
                <div class="placeholder-icon">
                    <i class="fas fa-user-plus fa-3x"></i>
                </div>
                <div class="placeholder-content">
                    <h4>Chọn khách hàng để xem gợi ý dinh dưỡng</h4>
                    <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem các gợi ý dinh dưỡng phù hợp</p>
                    <button onclick="scrollToCustomerSelection()" class="btn btn-outline-primary">
                        <i class="fas fa-arrow-up me-2"></i>Chọn khách hàng
                    </button>
                </div>
            </div>
        `;
        return;
    }

    console.log('✅ Starting API call for nutrition recommendations');

    // Show loading skeleton
    showNutritionLoadingSkeleton(contentContainer);

    try {
        const apiUrl = `/api/nutrition_recommendations?user_id=${userId}&nutrition_type=${nutritionType}&count=12`;
        console.log('🥗 API URL:', apiUrl);

        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        } const data = await response.json();
        console.log('✅ Nutrition data received:', data);
        console.log('✅ Number of recommendations:', data.recommendations?.length || 0);
        console.log('🔍 DEBUG - Data structure:', JSON.stringify(data, null, 2));
        console.log('🔍 DEBUG - About to call displayNutritionRecommendations with:', { data, nutritionType });

        displayNutritionRecommendations(data, nutritionType);

        if (typeof showModernToast === 'function') {
            showModernToast(`✅ Đã tải gợi ý dinh dưỡng cho ${translateNutritionType(nutritionType)}!`, 'success');
        }

    } catch (error) {
        console.error('❌ Error loading nutrition recommendations:', error);
        showNutritionError(contentContainer, error.message);

        if (typeof showModernToast === 'function') {
            showModernToast('❌ Có lỗi khi tải gợi ý dinh dưỡng!', 'error');
        }
    }

    console.log('🥗 === LOAD NUTRITION RECOMMENDATIONS ENDED ===');
}

// Display nutrition recommendations
function displayNutritionRecommendations(data, nutritionType) {
    console.log('🎨 === DISPLAY NUTRITION RECOMMENDATIONS STARTED ===');
    console.log('🎨 Parameters received:', { data, nutritionType });
    console.log('🎨 Data.recommendations length:', data?.recommendations?.length || 0);

    const contentContainer = document.getElementById('nutrition-recommendations');
    console.log('🎨 Container found:', !!contentContainer);
    console.log('🎨 Container ID:', contentContainer?.id);

    let html = `
        <div class="nutrition-header">
            <div class="nutrition-title">
                <i class="fas fa-heart me-2"></i>
                <h3>Gợi ý cho ${translateNutritionType(nutritionType)}</h3>
            </div>
            <div class="nutrition-focus">
                <i class="fas fa-info-circle me-2"></i>
                <span>${data.nutrition_focus || 'Dinh dưỡng cân bằng cho sức khỏe tốt'}</span>
            </div>
        </div>
        <div class="nutrition-grid">
    `;
    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach((rec, index) => {
            html += `
                <div class="nutrition-card" style="animation-delay: ${index * 100}ms">
                    <div class="nutrition-image">
                        <div class="nutrition-placeholder">
                            <i class="fas fa-utensils"></i>
                            <span class="nutrition-category">${translateNutritionType(nutritionType)}</span>
                        </div>
                        <div class="nutrition-badge">
                            <i class="fas fa-leaf"></i>
                        </div>
                    </div>
                    <div class="nutrition-content">
                        <h5 class="nutrition-name" title="${rec.recipe_name}">${truncateText(rec.recipe_name, 50)}</h5>
                        
                        <div class="nutrition-meta">
                            ${rec.difficulty ? `<span class="difficulty ${getDifficultyClass(rec.difficulty)}">${rec.difficulty}</span>` : ''}
                            ${rec.meal_time ? `<span class="meal-time ${getMealTimeClass(rec.meal_time)}">${translateMealTime(rec.meal_time)}</span>` : ''}
                        </div>
                        
                        <div class="nutrition-rating">
                            ${generateStars(rec.predicted_rating)}
                            <span class="rating-value">${rec.predicted_rating.toFixed(1)}</span>
                        </div>
                        
                        <div class="nutrition-details">
                            ${rec.estimated_calories ? `
                                <div class="nutrition-detail">
                                    <i class="fas fa-fire text-orange"></i>
                                    <span>${rec.estimated_calories} cal</span>
                                </div>
                            ` : ''}
                            
                            ${rec.preparation_time_minutes ? `
                                <div class="nutrition-detail">
                                    <i class="fas fa-clock text-primary"></i>
                                    <span>${rec.preparation_time_minutes} phút</span>
                                </div>
                            ` : ''}
                            
                            ${rec.estimated_price_vnd ? `
                                <div class="nutrition-detail">
                                    <i class="fas fa-tag text-success"></i>
                                    <span>${rec.estimated_price_vnd.toLocaleString()} VND</span>
                                </div>
                            ` : ''}
                        </div>
                        
                        <div class="nutrition-actions">
                            <a href="${rec.recipe_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="fas fa-book-open me-1"></i>Công thức
                            </a>
                            <button class="btn btn-success btn-sm add-to-meal" data-recipe='${JSON.stringify(rec)}'>
                                <i class="fas fa-plus me-1"></i>Thêm vào thực đơn
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html += `
            <div class="no-nutrition-results">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h4>Không tìm thấy gợi ý dinh dưỡng</h4>
                <p class="text-muted">Hãy thử chọn loại dinh dưỡng khác hoặc kiểm tra lại thông tin khách hàng.</p>
            </div>
        `;
    }
    html += `
        </div>
    `;    // Add fade-in animation
    contentContainer.style.opacity = '0';
    contentContainer.innerHTML = html;
    console.log('🎨 HTML content set, length:', html.length);
    console.log('🎨 Container innerHTML length after set:', contentContainer.innerHTML.length);

    setTimeout(() => {
        contentContainer.style.transition = 'opacity 0.5s ease';
        contentContainer.style.opacity = '1';
        console.log('🎨 Fade-in animation applied');

        // Add event listeners for "Add to meal" buttons
        contentContainer.querySelectorAll('.add-to-meal').forEach(btn => {
            btn.addEventListener('click', function () {
                const recipe = JSON.parse(this.getAttribute('data-recipe'));
                addToMealPlan(recipe);
            });
        });
        console.log('🎨 Event listeners added to Add to meal buttons');
    }, 100);

    console.log('🎨 === DISPLAY NUTRITION RECOMMENDATIONS ENDED ===');
}

// Load meal plans
async function loadMealPlans() {
    console.log('🍽️ === LOAD MEAL PLANS STARTED ===');
    console.log('🍽️ Loading meal plans...');

    const userIdElement = document.getElementById('userId');
    const userId = userIdElement?.value;
    const contentContainer = document.getElementById('meal-plans-content');

    console.log('🍽️ User ID element found:', !!userIdElement);
    console.log('🍽️ User ID value:', userId);
    console.log('🍽️ Meal plans container found:', !!contentContainer);

    if (!contentContainer) {
        console.error('❌ Meal plans container not found!');
        return;
    }

    if (!userId || userId === '') {
        console.log('ℹ️ No user ID selected, showing placeholder');
        // Show friendly message
        contentContainer.innerHTML = `
            <div class="meal-plans-placeholder">
                <div class="placeholder-icon">
                    <i class="fas fa-user-plus fa-3x"></i>
                </div>
                <div class="placeholder-content">
                    <h4>Chọn khách hàng để xem thực đơn gợi ý</h4>
                    <p class="text-muted">Vui lòng chọn khách hàng từ phần trên để xem thực đơn theo bữa phù hợp</p>
                    <button onclick="scrollToCustomerSelection()" class="btn btn-outline-primary">
                        <i class="fas fa-arrow-up me-2"></i>Chọn khách hàng
                    </button>
                </div>
            </div>
        `;
        return;
    }

    console.log('✅ Starting API call for meal plans');

    // Show loading skeleton
    showMealPlansLoadingSkeleton(contentContainer);

    try {
        const apiUrl = `/api/meal_plans?user_id=${userId}&days=3`;
        console.log('🍽️ API URL:', apiUrl);

        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        } const data = await response.json();
        console.log('✅ Meal plans data received:', data);
        console.log('✅ Number of meal plans:', data.meal_plans?.length || 0);
        console.log('🔍 DEBUG - Meal plans data structure:', JSON.stringify(data, null, 2));
        console.log('🔍 DEBUG - About to call displayMealPlans with:', data.meal_plans);

        displayMealPlans(data.meal_plans);

        if (typeof showModernToast === 'function') {
            showModernToast('✅ Đã tải thực đơn gợi ý thành công!', 'success');
        }

    } catch (error) {
        console.error('❌ Error loading meal plans:', error);
        showMealPlansError(contentContainer, error.message);

        if (typeof showModernToast === 'function') {
            showModernToast('❌ Có lỗi khi tải thực đơn!', 'error');
        }
    }

    console.log('🍽️ === LOAD MEAL PLANS ENDED ===');
}

// Display meal plans in the grid
function displayMealPlans(mealPlans) {
    console.log('🍽️ === DISPLAY MEAL PLANS STARTED ===');
    console.log('🍽️ Meal plans received:', mealPlans);
    console.log('🍽️ Meal plans length:', mealPlans?.length || 0);

    const contentContainer = document.getElementById('meal-plans-content');
    console.log('🍽️ Container found:', !!contentContainer);
    console.log('🍽️ Container ID:', contentContainer?.id);

    if (!mealPlans || mealPlans.length === 0) {
        contentContainer.innerHTML = `
            <div class="meal-plans-placeholder">
                <div class="placeholder-icon">
                    <i class="fas fa-calendar-times fa-4x"></i>
                </div>
                <div class="placeholder-content">
                    <h4>Không có thực đơn gợi ý</h4>
                    <p class="text-muted">Hãy thử với khách hàng khác hoặc liên hệ để được hỗ trợ</p>
                    <button class="btn btn-primary" onclick="loadMealPlans()">
                        <i class="fas fa-refresh me-2"></i>Thử lại
                    </button>
                </div>
            </div>
        `;
        return;
    }

    // Create horizontal scrollable meal plan layout
    let html = '';

    // Generate meal plan columns (up to 6 plans)
    const maxPlans = Math.min(mealPlans.length, 6);

    for (let i = 0; i < maxPlans; i++) {
        const plan = mealPlans[i];
        const isHighlighted = [1, 3, 5].includes(i); // Highlight plans 2, 4, 6 (0-indexed: 1, 3, 5)

        html += `
            <div class="meal-plan-column ${isHighlighted ? 'highlighted' : ''}" data-plan-index="${i}">
                <div class="meal-plan-header">
                    <div class="meal-plan-title">Thực đơn</div>
                    <div class="meal-plan-number">${i + 1}</div>
                </div>
                <div class="meal-plan-content">
                    ${generateMealSlots(plan)}
                </div>
            </div>
        `;
    }

    // Add fade-in animation
    contentContainer.style.opacity = '0';
    contentContainer.innerHTML = html;

    setTimeout(() => {
        contentContainer.style.transition = 'opacity 0.5s ease';
        contentContainer.style.opacity = '1';
        console.log('🍽️ Horizontal scrollable meal plans displayed');
    }, 100);

    console.log('🍽️ === DISPLAY MEAL PLANS ENDED ===');
}

// Helper function to generate meal slots for each meal plan column
function generateMealSlots(plan) {
    const mealTimes = ['breakfast', 'lunch', 'dinner'];
    let slotsHtml = '';

    mealTimes.forEach(mealTime => {
        const meal = plan[mealTime];

        if (meal && meal.recipe_name) {
            slotsHtml += `
                <div class="meal-slot" title="${meal.recipe_name}">
                    ${meal.image_url
                    ? `<img src="${meal.image_url}" alt="${meal.recipe_name}" class="meal-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                           <div class="meal-image-placeholder" style="display: none;">
                               <i class="fas fa-utensils"></i>
                           </div>`
                    : `<div class="meal-image-placeholder">
                               <i class="fas fa-utensils"></i>
                           </div>`
                }
                    <div class="meal-name">${truncateText(meal.recipe_name, 25)}</div>
                    ${meal.recipe_url
                    ? `<a href="${meal.recipe_url}" target="_blank" class="meal-detail-link">Chi tiết</a>`
                    : ''
                }
                </div>
            `;
        } else {
            slotsHtml += `
                <div class="meal-slot">
                    <div class="meal-image-placeholder">
                        <i class="fas fa-ban"></i>
                    </div>
                    <div class="meal-name empty-meal">Chưa có món</div>
                </div>
            `;
        }
    });

    return slotsHtml;
}

// Function to scroll meal plans horizontally
function scrollMealPlans(direction) {
    const scrollContainer = document.getElementById('meal-plans-content');
    if (!scrollContainer) return;

    const scrollAmount = 240; // Width of one meal plan column + gap
    const currentScroll = scrollContainer.scrollLeft;

    if (direction === 'left') {
        scrollContainer.scrollTo({
            left: currentScroll - scrollAmount,
            behavior: 'smooth'
        });
    } else {
        scrollContainer.scrollTo({
            left: currentScroll + scrollAmount,
            behavior: 'smooth'
        });
    }
}

// Helper functions for meal plans
function getMealTimeIcon(mealTime) {
    const icons = {
        'breakfast': 'fa-sun',
        'lunch': 'fa-cloud-sun',
        'dinner': 'fa-moon'
    };
    return icons[mealTime] || 'fa-utensils';
}

function translateMealTimeToVietnamese(mealTime) {
    const translations = {
        'breakfast': 'Bữa sáng',
        'lunch': 'Bữa trưa',
        'dinner': 'Bữa tối'
    };
    return translations[mealTime] || mealTime;
}

function selectMealPlan(planIndex) {
    showModernToast(`🗓️ Đã chọn thực đơn ${planIndex + 1}!`, 'success');

    // Add visual feedback
    const cards = document.querySelectorAll('.meal-plan-card');
    cards.forEach((card, index) => {
        if (index === planIndex) {
            card.style.border = '3px solid #28a745';
            card.style.boxShadow = '0 0 20px rgba(40, 167, 69, 0.3)';
        } else {
            card.style.border = '';
            card.style.boxShadow = '';
        }
    });
}

function addToMealPlan(recipe) {
    showModernToast(`🍽️ Đã thêm "${truncateText(recipe.recipe_name, 30)}" vào thực đơn!`, 'success');

    // Add visual feedback to the button
    const buttons = document.querySelectorAll('.add-to-meal');
    buttons.forEach(btn => {
        const btnRecipe = JSON.parse(btn.getAttribute('data-recipe'));
        if (btnRecipe.recipe_name === recipe.recipe_name) {
            btn.innerHTML = '<i class="fas fa-check me-1"></i>Đã thêm';
            btn.classList.remove('btn-success');
            btn.classList.add('btn-secondary');
            btn.disabled = true;
        }
    });
}

// Truncate text helper
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Scroll to customer selection
function scrollToCustomerSelection() {
    const customerSection = document.querySelector('.customer-select-wrapper');
    if (customerSection) {
        customerSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Add highlight effect
        customerSection.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.5)';
        setTimeout(() => {
            customerSection.style.boxShadow = '';
        }, 3000);
    }
}

// Manual trigger for testing - can be called from console
function manualTriggerNutritionAndMealPlans() {
    console.log('🧪 Manual trigger for nutrition and meal plans');
    reloadNutritionAndMealPlans();
}

// Test function to check if containers exist
function checkContainers() {
    const nutritionContainer = document.getElementById('nutrition-recommendations');
    const mealPlansContainer = document.getElementById('meal-plans-content');
    const userId = document.getElementById('userId')?.value;

    console.log('=== Container Check ===');
    console.log('Nutrition container:', !!nutritionContainer);
    console.log('Meal plans container:', !!mealPlansContainer);
    console.log('User ID:', userId);
    console.log('Nutrition container ID:', nutritionContainer?.id);
    console.log('Meal plans container ID:', mealPlansContainer?.id);

    if (nutritionContainer) {
        console.log('Nutrition container innerHTML length:', nutritionContainer.innerHTML.length);
    }
    if (mealPlansContainer) {
        console.log('Meal plans container innerHTML length:', mealPlansContainer.innerHTML.length);
    }
}

// === DEBUG FUNCTIONS ===
// Debug function to check customer selection and trigger nutrition/meal plans
function debugCustomerSelection() {
    console.log('🐛 === DEBUG CUSTOMER SELECTION ===');

    const userIdSelect = document.getElementById('userId');
    const nutritionContainer = document.getElementById('nutrition-recommendations');
    const mealPlansContainer = document.getElementById('meal-plans-content');

    console.log('User ID Select element:', !!userIdSelect);
    console.log('User ID Select value:', userIdSelect?.value);
    console.log('User ID Select options count:', userIdSelect?.options?.length);
    console.log('Nutrition container:', !!nutritionContainer);
    console.log('Meal plans container:', !!mealPlansContainer);

    if (userIdSelect) {
        console.log('Current selected option:', userIdSelect.options[userIdSelect.selectedIndex]?.textContent);
    }

    // Check if containers have content
    if (nutritionContainer) {
        console.log('Nutrition container content length:', nutritionContainer.innerHTML.length);
        console.log('Nutrition container content preview:', nutritionContainer.innerHTML.substring(0, 100) + '...');
    }

    if (mealPlansContainer) {
        console.log('Meal plans container content length:', mealPlansContainer.innerHTML.length);
        console.log('Meal plans container content preview:', mealPlansContainer.innerHTML.substring(0, 100) + '...');
    }

    console.log('🐛 === END DEBUG ===');
}

// Force trigger nutrition and meal plans reload
function forceReloadNutritionAndMealPlans() {
    console.log('🔥 Force triggering nutrition and meal plans reload...');

    const userIdSelect = document.getElementById('userId');
    console.log('User ID Select element:', userIdSelect);
    if (!userIdSelect || !userIdSelect.value) {
        console.log('❌ No customer selected, selecting first available customer...');
        const firstOption = userIdSelect?.querySelector('option[value!=""]');
        if (firstOption) {
            userIdSelect.value = firstOption.value;
            console.log('✅ Selected customer:', firstOption.textContent);
        }
    }

    // Force trigger the reload
    reloadNutritionAndMealPlans();
}

// Test API calls directly
async function testAPICalls() {
    console.log('🧪 Testing API calls directly...');

    const userIdSelect = document.getElementById('userId');
    const userId = userIdSelect?.value || 'CUS00001'; // Default to customer CUS00001

    console.log('Testing with User ID:', userId);

    // Test Nutrition API  
    try {
        const nutritionUrl = `/api/nutrition_recommendations?user_id=${userId}&nutrition_type=weight-loss&count=6`;
        console.log('📡 Nutrition API URL:', nutritionUrl);

        const nutritionResponse = await fetch(nutritionUrl);
        const nutritionData = await nutritionResponse.json();

        console.log('📡 Nutrition Response Status:', nutritionResponse.status);
        console.log('📡 Nutrition Data:', nutritionData);

        if (nutritionData.recommendations) {
            console.log('✅ Nutrition: Got', nutritionData.recommendations.length, 'recommendations');
        } else {
            console.log('❌ Nutrition: No recommendations found');
        }
    } catch (error) {
        console.error('❌ Nutrition API Error:', error);
    }

    // Test Meal Plans API
    try {
        const mealPlansUrl = `/api/meal_plans?user_id=${userId}&days=3`;
        console.log('📡 Meal Plans API URL:', mealPlansUrl);

        const mealPlansResponse = await fetch(mealPlansUrl);
        const mealPlansData = await mealPlansResponse.json();

        console.log('📡 Meal Plans Response Status:', mealPlansResponse.status);
        console.log('📡 Meal Plans Data:', mealPlansData);

        if (mealPlansData.meal_plans) {
            console.log('✅ Meal Plans: Got', mealPlansData.meal_plans.length, 'plans');
        } else {
            console.log('❌ Meal Plans: No plans found');
        }
    } catch (error) {
        console.error('❌ Meal Plans API Error:', error);
    }
}

// Test auto-load functionality
async function testAutoLoad() {
    console.log('🧪 === TESTING AUTO-LOAD FUNCTIONALITY ===');

    const userIdSelect = document.getElementById('userId');
    if (!userIdSelect) {
        console.error('❌ User ID select not found');
        return;
    }

    console.log('✅ User ID select found');
    console.log('📋 Available options:', Array.from(userIdSelect.options).map(opt => opt.textContent));

    // Test with first non-empty option
    let testOption = null;
    for (let i = 1; i < userIdSelect.options.length; i++) {
        if (userIdSelect.options[i].value) {
            testOption = userIdSelect.options[i];
            break;
        }
    }

    if (!testOption) {
        console.error('❌ No valid customer option found to test');
        return;
    }

    console.log('🎯 Testing with customer:', testOption.textContent);

    // Simulate selection
    userIdSelect.value = testOption.value;
    userIdSelect.dispatchEvent(new Event('change', { bubbles: true }));

    console.log('🔥 Change event dispatched, waiting for auto-load...');

    // Check results after delay
    setTimeout(() => {
        const nutritionContainer = document.getElementById('nutrition-recommendations');
        const mealPlansContainer = document.getElementById('meal-plans-content');

        console.log('📊 Nutrition container content length:', nutritionContainer?.innerHTML.length || 0);
        console.log('📊 Meal plans container content length:', mealPlansContainer?.innerHTML.length || 0);

        if (nutritionContainer?.innerHTML.includes('spinner-border')) {
            console.log('🔄 Still loading nutrition...');
        } else if (nutritionContainer?.innerHTML.includes('nutrition-placeholder')) {
            console.log('❌ Still showing nutrition placeholder');
        } else if (nutritionContainer?.innerHTML.length > 1000) {
            console.log('✅ Nutrition content loaded successfully');
        }

        if (mealPlansContainer?.innerHTML.includes('spinner-border')) {
            console.log('🔄 Still loading meal plans...');
        } else if (mealPlansContainer?.innerHTML.includes('meal-plans-placeholder')) {
            console.log('❌ Still showing meal plans placeholder');
        } else if (mealPlansContainer?.innerHTML.length > 1000) {
            console.log('✅ Meal plans content loaded successfully');
        }
    }, 3000);
}

// Expose debug functions to window for console access
window.debugCustomerSelection = debugCustomerSelection;
window.forceReloadNutritionAndMealPlans = forceReloadNutritionAndMealPlans;
window.testAPICalls = testAPICalls;
window.checkContainers = checkContainers;
window.manualTriggerNutritionAndMealPlans = manualTriggerNutritionAndMealPlans;
window.testAutoLoad = testAutoLoad;

console.log('🎉 Modern Vietnamese Food Recommendation System loaded successfully!');
console.log('🐛 Debug functions available: debugCustomerSelection(), forceReloadNutritionAndMealPlans(), testAPICalls()');
