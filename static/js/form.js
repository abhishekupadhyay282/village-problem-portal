/**
 * Form validation and dashboard interaction JavaScript
 */

// Form validation on submit
const problemForm = document.getElementById('problemForm');
if (problemForm) {
    problemForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        // Clear previous errors
        clearErrors();
        
        // Get form data
        const formData = new FormData(this);
        const name = formData.get('name').trim();
        const category = formData.get('category');
        const description = formData.get('description').trim();
        const contact = formData.get('contact').trim();
        
        // Validate form
        let isValid = true;
        
        if (!name) {
            showError('nameError', 'Name is required');
            isValid = false;
        } else if (name.length < 3) {
            showError('nameError', 'Name must be at least 3 characters');
            isValid = false;
        }
        
        if (!category) {
            showError('categoryError', 'Please select a category');
            isValid = false;
        }
        
        if (!description) {
            showError('descriptionError', 'Description is required');
            isValid = false;
        } else if (description.length < 10) {
            showError('descriptionError', 'Description must be at least 10 characters');
            isValid = false;
        }
        
        if (!contact) {
            showError('contactError', 'Contact information is required');
            isValid = false;
        } else if (!isValidContact(contact)) {
            showError('contactError', 'Please enter a valid phone or email');
            isValid = false;
        }
        
        if (!isValid) {
            return;
        }
        
        // Submit form
        submitForm(this);
    });
}

/**
 * Show error message for a field
 */
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

/**
 * Clear all error messages
 */
function clearErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });
    
    const errorAlert = document.getElementById('errorMessage');
    if (errorAlert) {
        errorAlert.style.display = 'none';
    }
}

/**
 * Validate email or phone
 */
function isValidContact(contact) {
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Simple phone validation (at least 10 digits)
    const phoneRegex = /^\d{10,}$/;
    
    const cleanPhone = contact.replace(/\D/g, '');
    
    return emailRegex.test(contact) || phoneRegex.test(cleanPhone) || contact.length >= 10;
}

/**
 * Submit form via AJAX
 */
function submitForm(form) {
    const formData = new FormData(form);
    
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            const successMessage = document.getElementById('successMessage');
            if (successMessage) {
                successMessage.style.display = 'block';
            }
            
            // Reset form
            form.reset();
            
            // Hide success message after 5 seconds
            setTimeout(() => {
                if (successMessage) {
                    successMessage.style.display = 'none';
                }
            }, 5000);
        } else {
            // Show error message
            const errorMessage = document.getElementById('errorMessage');
            if (errorMessage) {
                errorMessage.textContent = '❌ ' + data.message;
                errorMessage.style.display = 'block';
            }
        }
    })
    .catch(error => {
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
            errorMessage.textContent = '❌ An error occurred. Please try again.';
            errorMessage.style.display = 'block';
        }
        console.error('Error:', error);
    });
}

/**
 * Update problem status via API
 */
function updateStatus(selectElement) {
    const problemId = selectElement.getAttribute('data-problem-id');
    const newStatus = selectElement.value;
    
    fetch(`/api/problems/${problemId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Status updated successfully');
        } else {
            alert('Failed to update status: ' + data.message);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating status');
        location.reload();
    });
}

/**
 * Delete a problem via API
 */
function deleteProblem(problemId) {
    if (confirm('Are you sure you want to delete this problem?')) {
        fetch(`/api/problems/${problemId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload page to show updated list
                location.reload();
            } else {
                alert('Failed to delete problem: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting');
        });
    }
}
