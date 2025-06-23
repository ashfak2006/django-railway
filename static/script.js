document.addEventListener('DOMContentLoaded', function() {
    // Header background change on scroll
    const header = document.getElementById('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('bg-gray-900');
            header.classList.remove('bg-transparent');
        } else {
            header.classList.remove('bg-gray-900');
            header.classList.add('bg-transparent');
        }
    });
    const header_txt = document.getElementById('header_txt');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header_txt.classList.add('text-white');
            header_txt.classList.remove('text-primary');
        } else {
            header_txt.classList.remove('text-white');
            header_txt.classList.add('text-primary');
        }
    });
    
    // Initial header state check
    if (window.scrollY > 50) {
        header.classList.add('bg-gray-900');
        header.classList.remove('bg-transparent');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMenuButton = document.getElementById('close-menu-button');
    
    mobileMenuButton.addEventListener('click', function() {
        mobileMenu.classList.remove('-translate-x-full');
    });
    
    closeMenuButton.addEventListener('click', function() {
        mobileMenu.classList.add('-translate-x-full');
    });
    
    // Mobile shop submenu toggle
    const mobileShopButton = document.getElementById('mobile-shop-button');
    const mobileShopMenu = document.getElementById('mobile-shop-menu');
    
    mobileShopButton.addEventListener('click', function() {
        mobileShopMenu.classList.toggle('hidden');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Mobile filter toggle
    const filtersSidebar = document.getElementById('filters-sidebar');
    const mobileFilterToggle = document.getElementById('mobile-filter-toggle');
    
    mobileFilterToggle.addEventListener('click', function() {
        filtersSidebar.classList.toggle('h-0');
        filtersSidebar.classList.toggle('h-auto');
    });
    
    // Initialize as hidden on mobile
    if (window.innerWidth < 1024) {
        filtersSidebar.classList.add('h-0');
    }
    
    // Update on resize
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) {
            filtersSidebar.classList.remove('h-0');
            filtersSidebar.classList.add('h-auto');
        } else {
            filtersSidebar.classList.add('h-0');
        }
    });
});

//<----------------------------------------------product details------------------------------------>

document.addEventListener('DOMContentLoaded', function() {
    // Quantity selector
    const quantityInput = document.getElementById('quantityInput');
    const decrementBtn = document.getElementById('decrementBtn');
    const incrementBtn = document.getElementById('incrementBtn');
    
    decrementBtn.addEventListener('click', function() {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
    
    incrementBtn.addEventListener('click', function() {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
    
    // Image gallery
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Remove active class from all thumbnails
            thumbnails.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked thumbnail
            this.classList.add('active');
            
            // Update main image
            const index = this.getAttribute('data-index');
            const imgSrc = this.querySelector('img').src;
            mainImage.src = imgSrc.replace(/width=\d+&height=\d+/, 'width=600&height=600');
        });
    });
    
    // Image zoom functionality
    const zoomContainer = document.querySelector('.image-zoom-container');
    const zoomImage = document.querySelector('.image-zoom');
    
    if (zoomContainer && zoomImage) {
        zoomContainer.addEventListener('mousemove', function(e) {
            const rect = zoomContainer.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            zoomImage.style.setProperty('--x', x + '%');
            zoomImage.style.setProperty('--y', y + '%');
        });
    }
    
    // Related products carousel
    const carousel = document.getElementById('relatedProductsCarousel');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (carousel && prevBtn && nextBtn) {
        nextBtn.addEventListener('click', function() {
            carousel.scrollBy({ left: 300, behavior: 'smooth' });
        });
        
        prevBtn.addEventListener('click', function() {
            carousel.scrollBy({ left: -300, behavior: 'smooth' });
        });
    }
    
    // Sticky add to cart for mobile
    const stickyAddToCart = document.querySelector('.sticky-add-to-cart');
    
    if (stickyAddToCart && window.innerWidth < 768) {
        stickyAddToCart.classList.remove('hidden');
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                stickyAddToCart.classList.remove('hidden');
            } else {
                stickyAddToCart.classList.add('hidden');
            }
        });
    }
});

//----------------------------------------------------------checkout-----------------------------------


document.addEventListener('DOMContentLoaded', function() {
    // Checkbox functionality
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const indicator = checkbox.nextElementSibling.querySelector('div');
        
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                indicator.classList.remove('hidden');
            } else {
                indicator.classList.add('hidden');
            }
        });
        
        // Initialize state
        if (checkbox.checked) {
            indicator.classList.remove('hidden');
        } else {
            indicator.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Radio button functionality
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        const indicator = radio.nextElementSibling.querySelector('div');
        
        radio.addEventListener('change', function() {
            // Hide all indicators in the same group
            document.querySelectorAll(`input[name="${this.name}"]`).forEach(r => {
                const ind = r.nextElementSibling.querySelector('div');
                ind.classList.add('hidden');
            });
            
            // Show the selected one
            if (this.checked) {
                indicator.classList.remove('hidden');
            }
        });
        
        // Initialize state
        if (radio.checked) {
            indicator.classList.remove('hidden');
        } else {
            indicator.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Payment method tabs
    const creditCardBtn = document.getElementById('creditCardBtn');
    const paypalBtn = document.getElementById('paypalBtn');
    const creditCardForm = document.getElementById('creditCardForm');
    const paypalForm = document.getElementById('paypalForm');
    
    creditCardBtn.addEventListener('click', function() {
        creditCardBtn.classList.add('bg-gray-100', 'text-primary', 'border-b-2', 'border-primary');
        creditCardBtn.classList.remove('text-gray-500');
        paypalBtn.classList.remove('bg-gray-100', 'text-primary', 'border-b-2', 'border-primary');
        paypalBtn.classList.add('text-gray-500');
        
        creditCardForm.classList.remove('hidden');
        paypalForm.classList.add('hidden');
    });
    
    paypalBtn.addEventListener('click', function() {
        paypalBtn.classList.add('bg-gray-100', 'text-primary', 'border-b-2', 'border-primary');
        paypalBtn.classList.remove('text-gray-500');
        creditCardBtn.classList.remove('bg-gray-100', 'text-primary', 'border-b-2', 'border-primary');
        creditCardBtn.classList.add('text-gray-500');
        
        paypalForm.classList.remove('hidden');
        creditCardForm.classList.add('hidden');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Card input formatting
    const cardNumberInput = document.getElementById('cardNumber');
    const expiryDateInput = document.getElementById('expiryDate');
    const cvvInput = document.getElementById('cvv');
    
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 16) value = value.slice(0, 16);
            
            // Format with spaces
            const parts = [];
            for (let i = 0; i < value.length; i += 4) {
                parts.push(value.slice(i, i + 4));
            }
            
            e.target.value = parts.join(' ');
        });
    }
    
    if (expiryDateInput) {
        expiryDateInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 4) value = value.slice(0, 4);
            
            if (value.length > 2) {
                e.target.value = value.slice(0, 2) + '/' + value.slice(2);
            } else {
                e.target.value = value;
            }
        });
    }
    
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 4) value = value.slice(0, 4);
            e.target.value = value;
        });
    }
});
//<-------------------------------------------------cart page---------------------------------------->

document.addEventListener('DOMContentLoaded', function() {
    // Quantity adjustment function
    window.updateQuantity = function(itemId, change) {
        const input = document.getElementById(`${itemId}-qty`);
        let value = parseInt(input.value) + change;
        
        if (value < 1) value = 1;
        if (value > 99) value = 99;
        
        input.value = value;
    };
    
    // Prevent manual input of invalid values
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) this.value = 1;
            if (value > 99) this.value = 99;
        });
    });
});

//-------------------------------login logout----------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
    // Custom checkbox functionality
    const checkboxes = document.querySelectorAll('.toggle-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="checkbox"]');
            const checkIcon = this.querySelector('.check-icon');
            
            input.checked = !input.checked;
            
            if (input.checked) {
                this.classList.add('bg-primary');
                this.classList.remove('bg-gray-200');
                checkIcon.classList.remove('hidden');
            } else {
                this.classList.remove('bg-primary');
                this.classList.add('bg-gray-200');
                checkIcon.classList.add('hidden');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    switchTab('login');
});

function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');
    const formTitle = document.getElementById('form-title');
    const formSubtitle = document.getElementById('form-subtitle');
    
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        
        loginTab.classList.add('bg-primary', 'text-white');
        loginTab.classList.remove('bg-gray-100', 'text-gray-700');
        
        signupTab.classList.remove('bg-primary', 'text-white');
        signupTab.classList.add('bg-gray-100', 'text-gray-700');
        
        formTitle.textContent = 'Welcome Back';
        formSubtitle.textContent = 'Sign in to access your account';
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
        
        loginTab.classList.remove('bg-primary', 'text-white');
        loginTab.classList.add('bg-gray-100', 'text-gray-700');
        
        signupTab.classList.add('bg-primary', 'text-white');
        signupTab.classList.remove('bg-gray-100', 'text-gray-700');
        
        formTitle.textContent = 'Create Account';
        formSubtitle.textContent = 'Join us and start shopping today';
    }
}

function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    const iconElement = document.getElementById(`${inputId}-icon`);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        iconElement.classList.remove('ri-eye-off-line');
        iconElement.classList.add('ri-eye-line');
    } else {
        passwordInput.type = 'password';
        iconElement.classList.remove('ri-eye-line');
        iconElement.classList.add('ri-eye-off-line');
    }
}

//-------------------------------------------------------------------------account about------------------------------------------


document.addEventListener('DOMContentLoaded', function() {
    // Account Tab Navigation
    const accountTabs = document.querySelectorAll('.account-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    accountTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            accountTabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Address Type Toggle
    const addressTypeTabs = document.querySelectorAll('.address-type-tab');
    const addressTypeContents = document.querySelectorAll('.address-type-content');
    
    addressTypeTabs.forEach((tab, index) => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            addressTypeTabs.forEach(t => t.classList.remove('active', 'bg-white', 'shadow-sm'));
            addressTypeContents.forEach(c => c.classList.add('hidden'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active', 'bg-white', 'shadow-sm');
            addressTypeContents[index].classList.remove('hidden');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Gallery Filtering
    const galleryFilters = document.querySelectorAll('.gallery-filter');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            const filterValue = filter.getAttribute('data-filter');
            
            // Remove active class from all filters
            galleryFilters.forEach(f => f.classList.remove('active', 'bg-white', 'shadow-sm'));
            
            // Add active class to clicked filter
            filter.classList.add('active', 'bg-white', 'shadow-sm');
            
            // Filter gallery items
            galleryItems.forEach(item => {
                const itemCategory = item.getAttribute('data-category');
                
                if (filterValue === 'all' || filterValue === itemCategory) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Gallery Modal
    const modal = document.getElementById('gallery-modal');
    const modalImg = document.getElementById('modal-img');
    const modalClose = document.querySelector('.modal-close');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            modal.style.display = 'flex';
            modalImg.src = img.src;
        });
    });
    
    modalClose.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});