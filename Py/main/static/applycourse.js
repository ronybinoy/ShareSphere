
// Function to validate Course Name


// Function to validate First Name
function validateFirstName() {
    var firstName = document.getElementById('firstName').value.trim();
    var errorElement = document.getElementById('firstNamespan');
    if (firstName === '') {
        errorElement.textContent = 'First Name is required.';
        return false;
    }
    errorElement.textContent = '';
    return true;
}
function validateLastName() {
    var firstName = document.getElementById('firstName').value.trim();
    var errorElement = document.getElementById('firstNamespan');
    if (firstName === '') {
        errorElement.textContent = 'First Name is required.';
        return false;
    }
    errorElement.textContent = '';
    return true;
}


// Add more validation functions for other fields here

// Attach live validation event listeners to all fields
document.getElementById('firstName').addEventListener('input', validatefirstName);
document.getElementById('lastName').addEventListener('input', validatelastName);
document.getElementById('email').addEventListener('input', validateemail);
document.getElementById('gender').addEventListener('input', validategender);
document.getElementById('dateOfBirth').addEventListener('input', validatedateOfBirth);
document.getElementById('citizenship').addEventListener('input', validatecitizenship);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);
document.getElementById('lastName').addEventListener('input', validateLastName);



// Add more event listeners for other fields here

// Function to validate the entire form
function validateForm(event) {
    var isFormValid = true;
    // Call the validation functions for all fields
    if (!validateCourseName()) {
        isFormValid = false;
    }
    if (!validateFirstName()) {
        isFormValid = false;
    }
    // Add more validation function calls for other fields here

    // Check if the form is valid
    if (!isFormValid) {
        // Prevent form submission if there are validation errors
        event.preventDefault();
    }
}

// Add form submit event listener to trigger form validation
var form = document.querySelector('form');
form.addEventListener('submit', validateForm);
