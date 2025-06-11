document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 DOM loaded, starting initialization...');
    
    // Simple initialization without complex customer features first
    try {
        initModernUI();
        initDarkMode();
        initSmoothTransitions();
        initFormValidation();
        console.log('✅ Basic features initialized');
        
        // Try customer selection initialization
        setTimeout(() => {
            try {
                initSimpleCustomerSelection();
                console.log('✅ Customer selection initialized');
            } catch (error) {
                console.error('❌ Customer selection error:', error);
            }
        }, 500);
        
    } catch (error) {
        console.error('❌ Initialization error:', error);
    }
    
    // Navbar scroll effect and active state
    initNavbar();
    addNavbarShortcuts();
    
    // Show/hide additional options based on recommendation type
    const recommendationType = document.getElementById('recommendationType');
    const itemIdOption = document.getElementById('itemIdOption');
    const mainDishIdOption = document.getElementById('mainDishIdOption');
    const familySizeOption = document.getElementById('familySizeOption');
    const ageGroupOption = document.getElementById('ageGroupOption');    recommendationType.addEventListener('change', function () {
        // Hide all options first with fade out
        const allOptions = [itemIdOption, mainDishIdOption, familySizeOption, ageGroupOption];
        
        allOptions.forEach(option => {
            if (!option.classList.contains('d-none')) {
                option.style.animation = 'fadeOutUp 0.3s ease';
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
                    showOptionWithAnimation(itemIdOption);
                    break;
                case 'upsell_sides':
                    showOptionWithAnimation(mainDishIdOption);
                    break;
                case 'family_combos':
                    showOptionWithAnimation(familySizeOption);
                    break;
                case 'age_based':
                    showOptionWithAnimation(ageGroupOption);
                    break;
            }
        }, 150);
    });
    
    // Helper function to show options with animation
    function showOptionWithAnimation(option) {
        option.classList.remove('d-none');
        option.style.animation = 'fadeInUp 0.5s ease';
        setTimeout(() => {
            option.style.animation = '';
        }, 500);
    }

    // Form submission
    const form = document.getElementById('recommendationForm');
    const resultsContainer = document.getElementById('recommendationResults');    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        
        // Enhanced validation with better UX
        const userId = document.getElementById('userId').value;
        const type = recommendationType.value;
        
        if (!userId) {
            // Focus on customer select and show enhanced helper
            const userIdSelect = document.getElementById('userId');
            userIdSelect.focus();
            userIdSelect.classList.add('is-invalid');
            
            // Show customer selection helper with animation
            showCustomerSelectionHelper();
            
            // Scroll to customer selection smoothly
            userIdSelect.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            
            showToast('Vui lòng chọn khách hàng trước khi tiếp tục!', 'warning');
            return;
        }

        // Show loading skeleton instead of basic spinner
        showLoadingSkeleton(resultsContainer);

        let apiUrl = '/api/';
        let params = new URLSearchParams();
        params.append('user_id', userId);

        switch (type) {
            case 'upsell_combos':
                apiUrl += 'upsell_combos';
                params.append('item_id', document.getElementById('itemId').value);
                break;
            case 'upsell_sides':
                apiUrl += 'upsell_sides';
                params.append('main_dish_id', document.getElementById('mainDishId').value);
                break;
            case 'family_combos':
                apiUrl += 'family_combos';
                params.append('family_size', document.getElementById('familySize').value);
                break;
            case 'age_based':
                apiUrl += 'age_based_recommendations';
                params.append('age_group', document.getElementById('ageGroup').value);
                break;
        }        try {
            const response = await fetch(`${apiUrl}?${params.toString()}`);
            const data = await response.json();

            if (response.ok) {
                displayResults(data, type);
                showNavbarNotification('Gợi ý món ăn đã được tải thành công! 🎉', 'success');
            } else {
                resultsContainer.innerHTML = `<div class="col-12 alert alert-danger">Lỗi: ${data.error || 'Không thể lấy gợi ý món ăn'}</div>`;
                showNavbarNotification('Có lỗi xảy ra khi tải gợi ý', 'error');
            }
        } catch (error) {
            resultsContainer.innerHTML = `<div class="col-12 alert alert-danger">Lỗi: ${error.message}</div>`;
            showNavbarNotification('Lỗi kết nối - vui lòng thử lại', 'error');
        }
    });    // Load meal plans button event
    const loadMealPlansBtn = document.getElementById('loadMealPlans');
    if (loadMealPlansBtn) {
        loadMealPlansBtn.addEventListener('click', loadMealPlans);
    }    // Auto-load meal plans when customer ID changes
    const userIdSelect = document.getElementById('userId');
    if (userIdSelect) {
        userIdSelect.addEventListener('change', function () {
            if (this.value) {
                loadMealPlans();
                // Also reload nutrition recommendations with current selection
                const activeNutritionItem = document.querySelector('.nutrition-nav-item.active');
                if (activeNutritionItem) {
                    const nutritionType = activeNutritionItem.getAttribute('data-nutrition');
                    loadNutritionRecommendations(nutritionType);
                }
            }
        });

        // Auto-load meal plans on page load with first customer
        if (userIdSelect.value) {
            loadMealPlans();
        }
    }

    // Initial trigger to show the correct form fields
    recommendationType.dispatchEvent(new Event('change'));

    // Handle nutrition navigation
    const nutritionNavItems = document.querySelectorAll('.nutrition-nav-item');
    nutritionNavItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            nutritionNavItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
            
            // Load nutrition recommendations
            const nutritionType = this.getAttribute('data-nutrition');
            loadNutritionRecommendations(nutritionType);
        });
    });

    // Add quick navigation shortcuts
    addNavbarShortcuts();
});

// Display results based on recommendation type
function displayResults(data, type) {
    const resultsContainer = document.getElementById('recommendationResults');
    resultsContainer.innerHTML = '';

    let html = '';

    switch (type) {
        case 'upsell_combos':
            html = displayComboResults(data);
            break;
        case 'upsell_sides':
            html = displaySidesResults(data);
            break;
        case 'family_combos':
            html = displayFamilyResults(data);
            break;
        case 'age_based':
            html = displayAgeResults(data);
            break;
    }

    resultsContainer.innerHTML = html;
}

function displayComboResults(data) {
    let html = `
        <div class="col-12 mb-4">
            <h2>Combo món ăn được gợi ý</h2>
            <p class="text-muted">${data.message}</p>
        </div>
        <div class="col-12 combo-box p-3 mb-4">
            <h3>Combo giảm giá 10%</h3>
            <div class="row">
    `;

    data.combo_recommendations.forEach(item => {
        html += `
            <div class="col-md-4 mb-3">
                <div class="card recipe-card">
                    <div class="card-body">
                        <h5 class="card-title">${item.recipe_name}</h5>
                        <p class="card-text">
                            <a href="${item.recipe_url}" target="_blank" class="btn btn-sm btn-outline-primary">Xem công thức</a>
                            <span class="price float-end">${item.combo_price}</span>
                        </p>
                        <div class="rating">
                            ${'★'.repeat(Math.round(item.predicted_rating))}${'☆'.repeat(5 - Math.round(item.predicted_rating))}
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += `
            </div>
            <div class="text-center mt-3">
                <button class="btn btn-success">Đặt combo này</button>
            </div>
        </div>
    `;

    return html;
}

function displaySidesResults(data) {
    let html = `
        <div class="col-12 mb-4">
            <h2>Món phụ được gợi ý</h2>
            <p class="text-muted">${data.message}</p>
        </div>
        <div class="row">
    `;

    data.side_dish_recommendations.forEach(item => {
        html += `
            <div class="col-md-4 mb-3">
                <div class="card recipe-card">
                    <div class="card-body">
                        <h5 class="card-title">${item.recipe_name}</h5>
                        <p class="card-text">
                            <a href="${item.recipe_url}" target="_blank" class="btn btn-sm btn-outline-primary">Xem công thức</a>
                            <span class="price float-end">${item.side_price}</span>
                        </p>
                        <div class="rating">
                            ${'★'.repeat(Math.round(item.predicted_rating))}${'☆'.repeat(5 - Math.round(item.predicted_rating))}
                        </div>
                        <div class="mt-2">
                            <button class="btn btn-sm btn-success">Thêm vào giỏ hàng</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    return html;
}

function displayFamilyResults(data) {
    let html = `
        <div class="col-12 mb-4">
            <h2>Combo cho gia đình</h2>
            <p class="text-muted">${data.suitable_for} - Thời gian chuẩn bị: ${data.preparation_time}</p>
            <p class="price h4 text-center">Tổng giá: ${data.total_price}</p>
        </div>
    `;

    // Main dishes
    html += `
        <div class="col-12 family-combo-section">
            <h3>Món chính</h3>
            <div class="row">
    `;

    data.family_combo.main_dishes.forEach(dish => {
        html += createDishCard(dish);
    });

    html += `
            </div>
        </div>
    `;

    // Side dishes
    html += `
        <div class="col-12 family-combo-section">
            <h3>Món phụ</h3>
            <div class="row">
    `;

    data.family_combo.side_dishes.forEach(dish => {
        html += createDishCard(dish);
    });

    html += `
            </div>
        </div>
    `;

    // Desserts
    html += `
        <div class="col-12 family-combo-section">
            <h3>Món tráng miệng</h3>
            <div class="row">
    `;

    data.family_combo.desserts.forEach(dish => {
        html += createDishCard(dish);
    });

    html += `
            </div>
        </div>
        <div class="col-12 text-center mt-4">
            <button class="btn btn-lg btn-success">Đặt combo gia đình này</button>
        </div>
    `;

    return html;
}

function displayAgeResults(data) {
    let html = `
        <div class="col-12 mb-4">
            <h2>Món ăn phù hợp cho ${translateAgeGroup(data.age_group)}</h2>
            <div class="nutrition-focus mb-4">
                <h4>Dinh dưỡng tập trung:</h4>
                <p>${data.nutrition_focus}</p>
            </div>
        </div>
        <div class="row">
    `;

    data.recommendations.forEach(item => {
        html += `
            <div class="col-md-4 mb-3">
                <div class="card recipe-card">
                    <div class="card-body">
                        <h5 class="card-title">${item.recipe_name}</h5>
                        <div class="my-2">
                            <span class="difficulty ${getDifficultyClass(item.difficulty)}">${item.difficulty}</span>
                            <span class="meal-time ${getMealTimeClass(item.meal_time)}">${translateMealTime(item.meal_time)}</span>
                        </div>
                        <p class="card-text">
                            <a href="${item.recipe_url}" target="_blank" class="btn btn-sm btn-outline-primary">Xem công thức</a>
                        </p>
                        <div class="rating">
                            ${'★'.repeat(Math.round(item.predicted_rating))}${'☆'.repeat(5 - Math.round(item.predicted_rating))}
                        </div>
                        <div class="mt-2">
                            <button class="btn btn-sm btn-success">Thêm vào giỏ hàng</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    return html;
}

function createDishCard(dish) {
    return `
        <div class="col-md-4 mb-3">
            <div class="card recipe-card">
                <div class="card-body">
                    <h5 class="card-title">${dish.recipe_name}</h5>
                    <div class="my-2">
                        <span class="difficulty ${getDifficultyClass(dish.difficulty)}">${dish.difficulty}</span>
                    </div>
                    <p class="card-text">
                        <a href="${dish.recipe_url}" target="_blank" class="btn btn-sm btn-outline-primary">Xem công thức</a>
                    </p>
                    <div class="rating">
                        ${'★'.repeat(Math.round(dish.predicted_rating))}${'☆'.repeat(5 - Math.round(dish.predicted_rating))}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function getDifficultyClass(difficulty) {
    if (difficulty === 'Dễ') return 'difficulty-easy';
    if (difficulty === 'Trung bình') return 'difficulty-medium';
    return 'difficulty-hard';
}

function getMealTimeClass(mealTime) {
    if (mealTime === 'breakfast') return 'meal-time-breakfast';
    if (mealTime === 'lunch') return 'meal-time-lunch';
    if (mealTime === 'dinner') return 'meal-time-dinner';
    return 'meal-time-unknown';
}

function translateMealTime(mealTime) {
    if (mealTime === 'breakfast') return 'Bữa sáng';
    if (mealTime === 'lunch') return 'Bữa trưa';
    if (mealTime === 'dinner') return 'Bữa tối';
    return 'Không xác định';
}

function translateAgeGroup(ageGroup) {
    if (ageGroup === 'children') return 'Trẻ em';
    if (ageGroup === 'teenagers') return 'Thanh thiếu niên';
    if (ageGroup === 'adults') return 'Người lớn';
    if (ageGroup === 'elderly') return 'Người cao tuổi';
    return ageGroup;
}

// Load meal plans function
async function loadMealPlans() {
    const userId = document.getElementById('userId').value;
    const contentContainer = document.getElementById('meal-plans-content');

    if (!userId) {
        // Instead of alert, show a friendly message
        contentContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-user-plus fa-3x text-muted mb-3"></i>
                <p class="text-muted">Vui lòng chọn khách hàng để xem thực đơn gợi ý</p>
                <button onclick="document.getElementById('userId').focus()" class="btn btn-outline-primary">
                    <i class="fas fa-arrow-up me-2"></i>Chọn khách hàng
                </button>
            </div>
        `;
        return;
    }// Show loading skeleton
    const skeletonHTML = `
        <div class="meal-plans-skeleton">
            ${Array(6).fill().map(() => `
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
    contentContainer.innerHTML = skeletonHTML;

    try {
        const response = await fetch(`/api/meal_plans?user_id=${userId}`);
        const data = await response.json();

        if (response.ok) {
            displayMealPlans(data.meal_plans);
        } else {
            throw new Error(data.error || 'Lỗi khi tải thực đơn');
        }
    } catch (error) {
        console.error('Error loading meal plans:', error);
        contentContainer.innerHTML = `<div class="text-center py-4 text-danger"><p>Lỗi: ${error.message}</p><button class="btn btn-primary" onclick="loadMealPlans()">Thử lại</button></div>`;
    }
}

// Display meal plans in the grid
function displayMealPlans(mealPlans) {
    const contentContainer = document.getElementById('meal-plans-content');

    let html = '<div class="meal-plans-grid">';

    mealPlans.forEach((plan, index) => {
        const isActive = index === 1 || index === 3 || index === 5; // Thực đơn 2, 4, 6 active

        html += `
            <div class="menu-column ${isActive ? 'active-menu' : ''}">
                <div class="menu-header">Thực đơn: ${plan.menu_number}</div>
                
                <!-- Bữa sáng -->
                <div class="meal-card">
                    ${plan.breakfast ? `
                        <div class="placeholder-image">
                            Bữa sáng ${plan.menu_number}
                        </div>
                        <p class="meal-name" title="${plan.breakfast.recipe_name}">${truncateText(plan.breakfast.recipe_name, 25)}</p>
                    ` : `
                        <div class="placeholder-image">
                            Không có món
                        </div>
                        <p class="meal-name">Chưa có món sáng</p>
                    `}
                </div>
                
                <!-- Bữa trưa -->
                <div class="meal-card">
                    ${plan.lunch ? `
                        <div class="placeholder-image">
                            Bữa trưa ${plan.menu_number}
                        </div>
                        <p class="meal-name" title="${plan.lunch.recipe_name}">${truncateText(plan.lunch.recipe_name, 25)}</p>
                    ` : `
                        <div class="placeholder-image">
                            Không có món
                        </div>
                        <p class="meal-name">Chưa có món trưa</p>
                    `}
                </div>
                
                <!-- Bữa tối -->
                <div class="meal-card">
                    ${plan.dinner ? `
                        <div class="placeholder-image">
                            Bữa tối ${plan.menu_number}
                        </div>
                        <p class="meal-name" title="${plan.dinner.recipe_name}">${truncateText(plan.dinner.recipe_name, 25)}</p>
                    ` : `
                        <div class="placeholder-image">
                            Không có món
                        </div>
                        <p class="meal-name">Chưa có món tối</p>
                    `}
                </div>
                
                <button class="btn meal-detail-btn" 
                        onclick="showMealPlanDetails(${plan.menu_number}, ${JSON.stringify(plan).replace(/"/g, '&quot;')})">
                    Xem Chi tiết
                </button>
            </div>
        `;
    });

    html += '</div>';
    contentContainer.innerHTML = html;
}

// Show meal plan details
function showMealPlanDetails(menuNumber, planData) {
    let detailsHtml = `
        <div class="modal fade" id="mealPlanModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Chi tiết Thực đơn ${menuNumber}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
    `;

    if (planData.breakfast) {
        detailsHtml += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-header bg-info text-white">Bữa sáng</div>
                    <div class="card-body">
                        <h6>${planData.breakfast.recipe_name}</h6>
                        <p><small class="text-muted">Độ khó: ${planData.breakfast.difficulty}</small></p>
                        <p><small class="text-muted">Đánh giá dự đoán: ${planData.breakfast.predicted_rating.toFixed(1)}/5</small></p>
                        <a href="${planData.breakfast.recipe_url}" target="_blank" class="btn btn-sm btn-primary">Xem công thức</a>
                    </div>
                </div>
            </div>
        `;
    }

    if (planData.lunch) {
        detailsHtml += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-header bg-warning text-dark">Bữa trưa</div>
                    <div class="card-body">
                        <h6>${planData.lunch.recipe_name}</h6>
                        <p><small class="text-muted">Độ khó: ${planData.lunch.difficulty}</small></p>
                        <p><small class="text-muted">Đánh giá dự đoán: ${planData.lunch.predicted_rating.toFixed(1)}/5</small></p>
                        <a href="${planData.lunch.recipe_url}" target="_blank" class="btn btn-sm btn-primary">Xem công thức</a>
                    </div>
                </div>
            </div>
        `;
    }

    if (planData.dinner) {
        detailsHtml += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-header bg-dark text-white">Bữa tối</div>
                    <div class="card-body">
                        <h6>${planData.dinner.recipe_name}</h6>
                        <p><small class="text-muted">Độ khó: ${planData.dinner.difficulty}</small></p>
                        <p><small class="text-muted">Đánh giá dự đoán: ${planData.dinner.predicted_rating.toFixed(1)}/5</small></p>
                        <a href="${planData.dinner.recipe_url}" target="_blank" class="btn btn-sm btn-primary">Xem công thức</a>
                    </div>
                </div>
            </div>
        `;
    }

    detailsHtml += `
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                        <button type="button" class="btn btn-success">Chọn thực đơn này</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    const existingModal = document.getElementById('mealPlanModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', detailsHtml);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('mealPlanModal'));
    modal.show();
}

// Utility function to truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Load nutrition recommendations
async function loadNutritionRecommendations(nutritionType) {
    const userId = document.getElementById('userId').value;
    const contentContainer = document.getElementById('nutrition-recommendations');
    
    if (!userId) {
        // Show friendly message instead of alert
        contentContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-user-plus fa-3x text-muted mb-3"></i>
                <p class="text-muted">Vui lòng chọn khách hàng để xem gợi ý dinh dưỡng</p>
                <button onclick="document.getElementById('userId').focus()" class="btn btn-outline-primary">
                    <i class="fas fa-arrow-up me-2"></i>Chọn khách hàng
                </button>
            </div>
        `;
        return;
    }// Show loading skeleton
    showLoadingSkeleton(contentContainer);

    try {
        const response = await fetch(`/api/nutrition_recommendations?user_id=${userId}&nutrition_type=${nutritionType}&count=12`);
        const data = await response.json();

        if (response.ok) {
            displayNutritionRecommendations(data);
        } else {
            throw new Error(data.error || 'Lỗi khi tải gợi ý dinh dưỡng');
        }
    } catch (error) {
        console.error('Error loading nutrition recommendations:', error);
        contentContainer.innerHTML = `<div class="text-center py-4 text-danger"><p>Lỗi: ${error.message}</p><button class="btn btn-primary" onclick="loadNutritionRecommendations('${nutritionType}')">Thử lại</button></div>`;
    }
}

// Display nutrition recommendations
function displayNutritionRecommendations(data) {
    const contentContainer = document.getElementById('nutrition-recommendations');
    
    let html = `
        <div class="nutrition-info mb-4">
            <h4>Lợi ích dinh dưỡng:</h4>
            <p class="nutrition-focus-text">${data.nutrition_focus}</p>
        </div>
        <div class="row">
    `;
    
    data.recommendations.forEach((rec, index) => {
        html += `
            <div class="col-md-4 col-lg-3 mb-3">
                <div class="card recipe-card h-100">
                    <div class="placeholder-image" style="height: 150px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; text-align: center;">
                        ${rec.recipe_name.substring(0, 20)}...
                    </div>
                    <div class="card-body d-flex flex-column">
                        <h6 class="card-title" title="${rec.recipe_name}">${truncateText(rec.recipe_name, 40)}</h6>
                        <div class="my-2">
                            <span class="difficulty ${getDifficultyClass(rec.difficulty)}">${rec.difficulty}</span>
                            <span class="meal-time ${getMealTimeClass(rec.meal_time)}">${translateMealTime(rec.meal_time)}</span>
                        </div>                        <div class="rating mb-2">
                            ${'★'.repeat(Math.round(rec.predicted_rating))} ${rec.predicted_rating.toFixed(1)}
                        </div>
                        ${rec.estimated_calories ? `<div class="calories mb-1"><small>🔥 ${rec.estimated_calories} cal</small></div>` : ''}
                        ${rec.preparation_time_minutes ? `<div class="prep-time mb-1"><small>⏱️ ${rec.preparation_time_minutes} phút</small></div>` : ''}
                        ${rec.estimated_price_vnd ? `<div class="price mb-2"><small>💰 ${rec.estimated_price_vnd.toLocaleString()} VND</small></div>` : ''}
                        <a href="${rec.recipe_url}" target="_blank" class="btn btn-sm btn-primary mt-auto">Xem công thức</a>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += `
        </div>
    `;
    
    contentContainer.innerHTML = html;
}

// Auto-load nutrition recommendations on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-load with default nutrition type (weight-loss)
    setTimeout(() => {
        loadNutritionRecommendations('weight-loss');
    }, 1000);
});

// Modern UI initialization
function initModernUI() {
    // Add fade-in animation to sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('fade-in-up');
    });
    
    // Initialize form animations
    initFormAnimations();
    
    // Add loading state to buttons
    initButtonLoadingStates();
    
    // Initialize hero animations
    initHeroAnimations();
}

// Form animations
function initFormAnimations() {
    const formElements = document.querySelectorAll('.modern-select, .modern-input');
    
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        element.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Add floating label effect
        element.addEventListener('input', function() {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });
}

// Button loading states
function initButtonLoadingStates() {
    const submitBtn = document.querySelector('#recommendationForm button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        
        submitBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang xử lý...';
            this.disabled = true;
            
            // Re-enable after form submission
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    }
}

// Hero animations
function initHeroAnimations() {
    // Parallax effect for hero background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero-background');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
    
    // Typing effect for hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                heroTitle.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        
        // Start typing after page load
        setTimeout(typeWriter, 1000);
    }
}

// Enhanced navbar functionality
function initNavbar() {
    // Create scroll progress indicator
    createScrollProgressIndicator();
    
    // Enhanced mobile navbar behavior
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    // Navbar scroll effect
    const navbar = document.querySelector('#mainNavbar');
    
    window.addEventListener('scroll', function() {
        updateScrollProgress();
        
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Smooth scrolling for navbar links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Add ripple effect
                addRippleEffect(this, e);
            }
        });
    });
    
    // Close mobile menu when clicking on a nav link
    if (navLinks && navbarCollapse && navbarToggler) {
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.setAttribute('aria-expanded', 'false');
                }
            });
        });
        
        // Add click-outside-to-close for mobile menu
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
            
            if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
                navbarToggler.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // Update active nav item on scroll
    window.addEventListener('scroll', function() {
        updateActiveNavItem();
    });
}

// Add ripple effect to buttons
function addRippleEffect(element, event) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
    
    // Add ripple animation CSS if not exists
    if (!document.getElementById('ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Add quick navigation shortcuts
function addNavbarShortcuts() {
    // Add keyboard shortcuts for navigation
    document.addEventListener('keydown', function(event) {
        if (event.altKey) {
            switch(event.key) {
                case '1':
                    event.preventDefault();
                    quickNavTo('home');
                    break;
                case '2':
                    event.preventDefault();
                    quickNavTo('recommendations');
                    break;
                case '3':
                    event.preventDefault();
                    quickNavTo('nutrition');
                    break;
                case '4':
                    event.preventDefault();
                    quickNavTo('meal-plans');
                    break;
                case '5':
                    event.preventDefault();
                    quickNavTo('results');
                    break;
            }
        }
    });
    
    // Add quick search functionality
    addQuickSearch();
}

// Add quick search to navbar
function addQuickSearch() {
    const navbar = document.querySelector('.navbar .container');
    const searchContainer = document.createElement('div');
    searchContainer.className = 'navbar-search d-none d-lg-block';
    searchContainer.style.cssText = `
        position: absolute;
        right: 120px;
        top: 50%;
        transform: translateY(-50%);
    `;
    
    searchContainer.innerHTML = `
        <div class="input-group input-group-sm" style="width: 200px;">
            <input type="text" class="form-control" placeholder="Tìm kiếm..." id="navbarSearch">
            <button class="btn btn-outline-light" type="button" id="searchBtn">
                <i class="fas fa-search"></i>
            </button>
        </div>
    `;
    
    navbar.appendChild(searchContainer);
    
    // Add search functionality
    const searchInput = document.getElementById('navbarSearch');
    const searchBtn = document.getElementById('searchBtn');
    
    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();
        if (!query) return;
        
        // Simple search through sections
        const sections = document.querySelectorAll('section, div[id]');
        let found = false;
        
        sections.forEach(section => {
            if (section.textContent.toLowerCase().includes(query)) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                found = true;
                return;
            }
        });
        
        if (!found) {
            // Show toast notification
            showToast('Không tìm thấy kết quả cho: ' + query, 'warning');
        }
        
        searchInput.value = '';
    }
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
}

// Enhanced Toast Notification System
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    
    toast.innerHTML = `
        <div class="toast-content">
            <i class="${icons[type] || icons.info}"></i>
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.closest('.toast-notification').remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="toast-progress"></div>
    `;
    
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: white;
        color: #333;
        padding: 0;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        z-index: 10000;
        min-width: 300px;
        max-width: 400px;
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border-left: 4px solid ${colors[type] || colors.info};
        overflow: hidden;
    `;
    
    // Add toast styles if not already present
    if (!document.querySelector('#toastStyles')) {
        const style = document.createElement('style');
        style.id = 'toastStyles';
        style.textContent = `
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
            
            .toast-content {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 16px 20px;
            }
            
            .toast-message {
                flex: 1;
                font-weight: 500;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .toast-close {
                background: none;
                border: none;
                color: #666;
                cursor: pointer;
                padding: 4px;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
            }
            
            .toast-close:hover {
                background: #f8f9fa;
                color: #333;
            }
            
            .toast-progress {
                height: 3px;
                background: ${colors[type] || colors.info};
                animation: progress ${duration}ms linear;
                transform-origin: left;
            }
            
            @keyframes progress {
                from { transform: scaleX(1); }
                to { transform: scaleX(0); }
            }
            
            .dark-mode .toast-notification {
                background: #2c3e50;
                color: #ecf0f1;
            }
            
            .dark-mode .toast-close:hover {
                background: #34495e;
                color: #ecf0f1;
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
    
    return toast;
}

// Enhanced navbar with loading indicator
function showNavbarLoading() {
    const navbar = document.querySelector('.navbar');
    navbar.style.opacity = '0.8';
}

function hideNavbarLoading() {
    const navbar = document.querySelector('.navbar');
    navbar.style.opacity = '1';
}

// Enhanced notification system for navbar
function showNavbarNotification(message, type = 'success', duration = 3000) {
    // Create notification badge
    const navbar = document.querySelector('.navbar');
    const notification = document.createElement('div');
    notification.className = `navbar-notification notification-${type}`;
    notification.style.cssText = `
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideDownFade 0.3s ease;
        max-width: 300px;
        text-align: center;
    `;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
    `;
    
    navbar.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideUpFade 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, duration);
}

// Add CSS for navbar notifications
function addNotificationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDownFade {
            0% {
                opacity: 0;
                transform: translateX(-50%) translateY(-10px);
            }
            100% {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        
        @keyframes slideUpFade {
            0% {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
            100% {
                opacity: 0;
                transform: translateX(-50%) translateY(-10px);
            }
        }
        
        .navbar-notification {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    `;
    document.head.appendChild(style);
}

// Initialize notification system
document.addEventListener('DOMContentLoaded', function() {
    addNotificationStyles();
    
    // Show welcome notification
    setTimeout(() => {
        showNavbarNotification('Chào mừng đến với hệ thống gợi ý món ăn! 🍽️', 'success', 4000);
    }, 1000);
});

// Add particles effect to hero section
function createParticlesEffect() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 1;
        pointer-events: none;
    `;
    
    // Create floating particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 10 + 5}px;
            height: ${Math.random() * 10 + 5}px;
            background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: floatParticle ${Math.random() * 20 + 10}s infinite linear;
            animation-delay: ${Math.random() * 10}s;
        `;
        particlesContainer.appendChild(particle);
    }
    
    heroSection.appendChild(particlesContainer);
    
    // Add particle animation CSS
    if (!document.getElementById('particle-styles')) {
        const style = document.createElement('style');
        style.id = 'particle-styles';
        style.textContent = `
            @keyframes floatParticle {
                0% {
                    transform: translateY(100vh) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Loading skeleton function
function showLoadingSkeleton(container) {
    const skeletonHTML = `
        <div class="loading-skeleton">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <div class="skeleton-card">
                        <div class="skeleton-header"></div>
                        <div class="skeleton-line"></div>
                        <div class="skeleton-line short"></div>
                        <div class="skeleton-button"></div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="skeleton-card">
                        <div class="skeleton-header"></div>
                        <div class="skeleton-line"></div>
                        <div class="skeleton-line short"></div>
                        <div class="skeleton-button"></div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="skeleton-card">
                        <div class="skeleton-header"></div>
                        <div class="skeleton-line"></div>
                        <div class="skeleton-line short"></div>
                        <div class="skeleton-button"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.innerHTML = skeletonHTML;
}

// Enhanced form submission with better UX
function enhancedFormSubmission() {
    const form = document.getElementById('recommendationForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Check if customer is selected
        const userId = document.getElementById('userId').value;
        if (!userId) {
            // Focus on customer select and show helper
            const userIdSelect = document.getElementById('userId');
            userIdSelect.focus();
            userIdSelect.classList.add('is-invalid');
            
            // Show customer selection helper
            showCustomerSelectionHelper();
            return;
        }
        
        // Continue with normal form submission
        handleFormSubmission();
    });
}

function showCustomerSelectionHelper() {
    // Remove any existing helper
    const existingHelper = document.querySelector('.customer-selection-helper');
    if (existingHelper) {
        existingHelper.remove();
    }
    
    const helper = document.createElement('div');
    helper.className = 'customer-selection-helper';
    helper.innerHTML = `
        <div class="helper-content">
            <i class="fas fa-arrow-up helper-arrow"></i>
            <p><strong>Vui lòng chọn khách hàng</strong></p>
            <p class="helper-subtitle">Sử dụng dropdown hoặc các nút chọn nhanh bên dưới</p>
        </div>
    `;
    
    helper.style.cssText = `
        position: absolute;
        top: -80px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 500;
        z-index: 10;
        animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        min-width: 280px;
        text-align: center;
    `;
    
    // Add bounce animation keyframes if not already present
    if (!document.querySelector('#bounceInKeyframes')) {
        const style = document.createElement('style');
        style.id = 'bounceInKeyframes';
        style.textContent = `
            @keyframes bounceIn {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) scale(0.3);
                }
                50% {
                    opacity: 1;
                    transform: translateX(-50%) scale(1.1);
                }
                100% {
                    opacity: 1;
                    transform: translateX(-50%) scale(1);
                }
            }
            .helper-subtitle {
                font-size: 0.8rem;
                opacity: 0.9;
                margin-top: 0.25rem;
                margin-bottom: 0;
                font-weight: 400;
            }
            .helper-arrow {
                font-size: 1.2rem;
                margin-bottom: 0.5rem;
                display: block;
                animation: bounce 2s infinite;
            }
        `;
        document.head.appendChild(style);
    }
    
    const customerWrapper = document.querySelector('.customer-select-wrapper');
    customerWrapper.style.position = 'relative';
    customerWrapper.appendChild(helper);
    
    // Remove helper after 5 seconds with fade out
    setTimeout(() => {
        if (helper.parentNode) {
            helper.style.animation = 'fadeOut 0.4s ease';
            setTimeout(() => helper.remove(), 400);
        }
    }, 5000);
    
    // Remove invalid state and helper when user selects
    const userIdSelect = document.getElementById('userId');
    const removeHelper = function() {
        userIdSelect.classList.remove('is-invalid');
        if (helper.parentNode) {
            helper.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => helper.remove(), 300);
        }
    };
    
    userIdSelect.addEventListener('change', removeHelper, { once: true });
    
    // Also remove when quick selection buttons are used
    document.querySelectorAll('.quick-customer-btn').forEach(btn => {
        btn.addEventListener('click', removeHelper, { once: true });
    });
}

// Simple Customer Selection - Minimal Implementation
function initSimpleCustomerSelection() {
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
    
    // Check if elements exist
    console.log('Elements found:', {
        userIdSelect: !!userIdSelect,
        customerInfo: !!customerInfo,
        randomBtn: !!randomBtn,
        firstBtn: !!firstBtn,
        vipBtn: !!vipBtn,
        toggleSearchBtn: !!toggleSearchBtn,
        searchBox: !!searchBox
    });
    
    if (!userIdSelect) {
        console.error('User select element not found!');
        return;
    }
    
    // Toggle search box with smooth animation
    if (toggleSearchBtn && searchBox) {
        toggleSearchBtn.addEventListener('click', function() {
            searchBox.classList.toggle('active');
            const isActive = searchBox.classList.contains('active');
            toggleSearchBtn.innerHTML = isActive 
                ? '<i class="fas fa-times me-1"></i>Đóng' 
                : '<i class="fas fa-search me-1"></i>Tìm kiếm';
            
            if (isActive && searchInput) {
                setTimeout(() => searchInput.focus(), 300);
            }
        });
    }
    
    // Enhanced search functionality
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
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
            
            searchResults.innerHTML = matches.length ? 
                matches.slice(0, 10).map(option => `
                    <div class="search-result-item" data-value="${option.value}">
                        ${option.textContent}
                    </div>
                `).join('') : 
                '<div class="search-result-item">Không tìm thấy khách hàng</div>';
                
            // Add click handlers to search results
            searchResults.querySelectorAll('.search-result-item[data-value]').forEach(item => {
                item.addEventListener('click', function() {
                    const value = this.getAttribute('data-value');
                    const text = this.textContent;
                    userIdSelect.value = value;
                    updateSimpleCustomerInfo(value, text);
                    searchInput.value = '';
                    searchResults.innerHTML = '';
                    searchBox.classList.remove('active');
                    toggleSearchBtn.innerHTML = '<i class="fas fa-search me-1"></i>Tìm kiếm';
                    showSimpleToast('Đã chọn: ' + text, 'success');
                });
            });
        });
    }
    
    // Quick selection buttons with enhanced feedback
    if (randomBtn) {
        randomBtn.addEventListener('click', function() {
            const options = userIdSelect.querySelectorAll('option[value!=""]');
            if (options.length > 0) {
                const randomOption = options[Math.floor(Math.random() * options.length)];
                userIdSelect.value = randomOption.value;
                updateSimpleCustomerInfo(randomOption.value, randomOption.textContent);
                showSimpleToast('🎲 Đã chọn khách hàng ngẫu nhiên!', 'success');
                
                // Add visual feedback
                randomBtn.style.transform = 'scale(0.95)';
                setTimeout(() => randomBtn.style.transform = '', 150);
            }
        });
    }
    
    if (firstBtn) {
        firstBtn.addEventListener('click', function() {
            const firstOption = userIdSelect.querySelector('option[value!=""]');
            if (firstOption) {
                userIdSelect.value = firstOption.value;
                updateSimpleCustomerInfo(firstOption.value, firstOption.textContent);
                showSimpleToast('👤 Đã chọn khách hàng đầu tiên!', 'info');
                
                firstBtn.style.transform = 'scale(0.95)';
                setTimeout(() => firstBtn.style.transform = '', 150);
            }
        });
    }
    
    if (vipBtn) {
        vipBtn.addEventListener('click', function() {
            // Just select a random customer and call it VIP
            const options = userIdSelect.querySelectorAll('option[value!=""]');
            if (options.length > 0) {
                const randomOption = options[Math.floor(Math.random() * options.length)];
                userIdSelect.value = randomOption.value;
                updateSimpleCustomerInfo(randomOption.value, randomOption.textContent + ' (VIP)');
                showSimpleToast('Đã chọn khách hàng VIP!', 'success');
            }
        });
    }
    
    if (toggleSearchBtn && searchBox) {
        toggleSearchBtn.addEventListener('click', function() {
            if (searchBox.style.display === 'none' || !searchBox.style.display) {
                searchBox.style.display = 'block';
                toggleSearchBtn.innerHTML = '<i class="fas fa-times me-1"></i>Đóng';
            } else {
                searchBox.style.display = 'none';
                toggleSearchBtn.innerHTML = '<i class="fas fa-search me-1"></i>Tìm kiếm';
            }
        });
    }
    
    // Handle select change
    userIdSelect.addEventListener('change', function() {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            updateSimpleCustomerInfo(this.value, selectedOption.textContent);
        }
    });
    
    console.log('Simple customer selection initialized successfully!');
}

function updateSimpleCustomerInfo(customerId, customerText) {
    const customerInfo = document.getElementById('customerInfo');
    if (customerInfo) {
        customerInfo.innerHTML = `
            <i class="fas fa-user me-2"></i>
            <strong>Đã chọn:</strong> ${customerText}
            <br><small class="text-muted">ID: ${customerId}</small>
        `;
        customerInfo.style.background = '#d4edda';
        customerInfo.style.color = '#155724';
        customerInfo.style.border = '1px solid #c3e6cb';
    }
}

function showSimpleToast(message, type) {
    // Simple alert replacement
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 9999;
        font-weight: 500;
        max-width: 300px;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ...existing code...
