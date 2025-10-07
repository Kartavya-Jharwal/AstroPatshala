// JavaScript for Chaldean Numerology Calculator

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Calculating...';
                submitBtn.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });

    // Add smooth scrolling to all links
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

    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Quick calculator functionality
    if (document.getElementById('quickCalculator')) {
        setupQuickCalculator();
    }

    // Form validation enhancements
    setupFormValidation();
});

function setupQuickCalculator() {
    const quickForm = document.getElementById('quickCalculator');
    const quickInput = document.getElementById('quickText');
    const quickResult = document.getElementById('quickResult');

    quickInput.addEventListener('input', debounce(function() {
        const text = this.value.trim();
        if (text.length > 0) {
            calculateQuick(text);
        } else {
            quickResult.style.display = 'none';
        }
    }, 300));

    async function calculateQuick(text) {
        try {
            const response = await fetch('/quick-calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error('Calculation failed');
            }

            const result = await response.json();
            displayQuickResult(result);
        } catch (error) {
            console.error('Quick calculation error:', error);
        }
    }

    function displayQuickResult(result) {
        const html = `
            <div class="alert alert-info">
                <h6>Quick Calculation for "${result.text}"</h6>
                <p class="mb-1"><strong>Number:</strong> ${result.reduced_number} ${result.compound_number !== result.reduced_number ? '(from ' + result.compound_number + ')' : ''}</p>
                <p class="mb-0"><strong>Meaning:</strong> ${result.interpretation.traits}</p>
            </div>
        `;
        quickResult.innerHTML = html;
        quickResult.style.display = 'block';
    }
}

function setupFormValidation() {
    // Add real-time validation to date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateDateInput(this);
        });
    });

    // Add real-time validation to name inputs
    const nameInputs = document.querySelectorAll('input[name*="name"]');
    nameInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNameInput(this);
        });
    });
}

function validateDateInput(input) {
    const date = new Date(input.value);
    const now = new Date();
    const minDate = new Date('1900-01-01');

    input.classList.remove('is-valid', 'is-invalid');

    if (!input.value) {
        return;
    }

    if (date > now) {
        input.classList.add('is-invalid');
        showInputError(input, 'Birth date cannot be in the future');
    } else if (date < minDate) {
        input.classList.add('is-invalid');
        showInputError(input, 'Birth date cannot be before 1900');
    } else {
        input.classList.add('is-valid');
        hideInputError(input);
    }
}

function validateNameInput(input) {
    const value = input.value.trim();
    const nameRegex = /^[a-zA-Z\s\-']+$/;

    input.classList.remove('is-valid', 'is-invalid');

    if (!value) {
        return;
    }

    if (!nameRegex.test(value)) {
        input.classList.add('is-invalid');
        showInputError(input, 'Name can only contain letters, spaces, hyphens, and apostrophes');
    } else if (value.length < 2) {
        input.classList.add('is-invalid');
        showInputError(input, 'Name must be at least 2 characters long');
    } else {
        input.classList.add('is-valid');
        hideInputError(input);
    }
}

function showInputError(input, message) {
    let errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function hideInputError(input) {
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Smart user search functionality
async function searchUsers() {
    const searchInput = document.getElementById('quickSearch');
    const searchResults = document.getElementById('searchResults');
    const query = searchInput.value.trim();
    
    if (!query) {
        searchResults.innerHTML = '';
        return;
    }
    
    try {
        const response = await fetch(`/quick-lookup?name=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.matches && data.matches.length > 0) {
            let html = '<div class="list-group list-group-flush">';
            
            data.matches.forEach(user => {
                const lastAccess = new Date(user.last_access).toLocaleDateString();
                const numbers = user.quick_numbers;
                const numbersText = Object.keys(numbers).length > 0 
                    ? `(${Object.entries(numbers).map(([k,v]) => `${k}: ${v}`).join(', ')})` 
                    : '';
                
                html += `
                    <a href="#" class="list-group-item list-group-item-action" 
                       onclick="loadUser('${user.name}', '${user.birth_date.split('T')[0]}')">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">${user.name}</h6>
                            <small class="text-muted">${lastAccess}</small>
                        </div>
                        <p class="mb-1">Born: ${user.birth_date.split('T')[0]} ${numbersText}</p>
                        <small class="text-muted">Accessed ${user.access_count} times</small>
                    </a>
                `;
            });
            
            html += '</div>';
            searchResults.innerHTML = html;
        } else {
            searchResults.innerHTML = '<div class="text-muted"><i class="fas fa-search me-2"></i>No matches found</div>';
        }
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = '<div class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Search failed</div>';
    }
}

// Load user calculation
async function loadUser(name, birthDate) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/load-user';
    form.style.display = 'none';
    
    const nameInput = document.createElement('input');
    nameInput.name = 'user_name';
    nameInput.value = name;
    
    const dateInput = document.createElement('input');
    dateInput.name = 'user_birth_date';
    dateInput.value = birthDate;
    
    form.appendChild(nameInput);
    form.appendChild(dateInput);
    document.body.appendChild(form);
    form.submit();
}

// Enhanced search with Enter key support
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('quickSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                searchUsers();
            } else if (this.value.length >= 2) {
                // Auto-search after 2+ characters
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(searchUsers, 300);
            } else if (this.value.length === 0) {
                document.getElementById('searchResults').innerHTML = '';
            }
        });
    }
    
    // Smart form enhancements
    const smartForm = document.getElementById('smartForm');
    if (smartForm) {
        const naturalInput = document.getElementById('natural_input');
        
        // Add real-time feedback
        naturalInput.addEventListener('input', function() {
            // Simple validation feedback
            const text = this.value.toLowerCase();
            const hasName = /name|call|i am/.test(text);
            const hasDate = /born|birth|birthday|\d{4}|\d{1,2}\/\d{1,2}/.test(text);
            
            let feedback = '';
            if (text.length > 10) {
                if (hasName && hasDate) {
                    feedback = '<i class="fas fa-check text-success me-2"></i>Looking good! Name and date detected.';
                } else if (hasName) {
                    feedback = '<i class="fas fa-info text-warning me-2"></i>Name detected. Please add your birth date.';
                } else if (hasDate) {
                    feedback = '<i class="fas fa-info text-warning me-2"></i>Date detected. Please add your name.';
                } else {
                    feedback = '<i class="fas fa-lightbulb text-info me-2"></i>Try: "My name is [Your Name] born [Date]"';
                }
            }
            
            const feedbackDiv = document.getElementById('smartFeedback') || 
                               (() => {
                                   const div = document.createElement('div');
                                   div.id = 'smartFeedback';
                                   div.className = 'form-text mt-2';
                                   naturalInput.parentNode.appendChild(div);
                                   return div;
                               })();
            
            feedbackDiv.innerHTML = feedback;
        });
    }
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Chaldean chart helper
const chaldeanChart = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5,
    'U': 6, 'V': 6, 'W': 6, 'X': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
};

// Function to add interactive chart if needed
function displayChaldeanChart() {
    const chartContainer = document.getElementById('chaldeanChart');
    if (!chartContainer) return;

    let chartHTML = '<div class="row">';
    for (let i = 1; i <= 8; i++) {
        const letters = Object.keys(chaldeanChart).filter(letter => chaldeanChart[letter] === i);
        chartHTML += `
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title text-primary">${i}</h5>
                        <p class="card-text">${letters.join(', ')}</p>
                    </div>
                </div>
            </div>
        `;
    }
    chartHTML += '</div>';
    chartContainer.innerHTML = chartHTML;
}

// Initialize chart if container exists
if (document.getElementById('chaldeanChart')) {
    displayChaldeanChart();
}

// Add click-to-copy functionality for results
document.addEventListener('click', function(e) {
    if (e.target.matches('.copy-result')) {
        const textToCopy = e.target.dataset.copyText;
        navigator.clipboard.writeText(textToCopy).then(function() {
            e.target.textContent = 'Copied!';
            setTimeout(() => {
                e.target.textContent = 'Copy';
            }, 2000);
        });
    }
});

// Easter egg for the sacred number 9
function addSacredNumberEffect() {
    const nineElements = document.querySelectorAll('[data-number="9"]');
    nineElements.forEach(element => {
        element.classList.add('sacred-number');
        element.setAttribute('data-bs-toggle', 'tooltip');
        element.setAttribute('title', 'The Sacred Number - Universal Love and Completion');
    });
}
