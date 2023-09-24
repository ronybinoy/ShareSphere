$(document).ready(function () {
    const fields = [
        { id: "#course_name", validate: validatecourse_name },
        { id: "#course_mode", validate: validatecourse_mode },
        { id: "#course_type", validate: validatecourse_type },
        { id: "#academic_disciplines", validate: validateacademic_disciplines },
        { id: "#course_desc", validate: validatecourse_desc },
        { id: "#eligibility", validate: validateeligibility },
        { id: "#fees", validate: validatefees },
        { id: "#duration", validate: validateduration },
        { id: "#opendate", validate: validateopendate },
        { id: "#appdeadline", validate: validateappdeadline },
        { id: "#thumbnail_image", validate: validatethumbnail_image },
        { id: "#seats_available", validate: validateseat_available }
    ];

    // Helper function to create an error message span
    function createErrorSpan(fieldId) {
        const errorSpanId = `${fieldId}span`;
        const $errorSpan = $(`<span id="${errorSpanId}" class="error-message"></span>`);
        $(fieldId).after($errorSpan);
        return $errorSpan;
    }

    // Helper function to display error messages
    function displayErrorMessage(fieldId, message) {
        const $errorSpan = $(`${fieldId}span`);
        $errorSpan.html(message).css("color", "#FF0000");
    }

    // Helper function to enable or disable the submit button based on form validity
    function enableSubmitButton() {
        const isValid = fields.every(field => {
            const $field = $(field.id);
            const $errorSpan = $(`${field.id}span`);

            if ($field.val().trim() === "" || $errorSpan.html() !== "") {
                return false;
            }
            return true;
        });

        // Validate the date range here
        if (!validateDateRange()) {
            isValid = false;
        }

        $("#submitBtn").prop("disabled", !isValid);
    }

    // Helper function to validate a field on blur
    function validateFieldOnBlur(fieldId, validationFunction) {
        $(fieldId).blur(function () {
            validationFunction();
        });
    }

    // Initialize error message spans and field validation on blur
    fields.forEach(field => {
        createErrorSpan(field.id);
        validateFieldOnBlur(field.id, field.validate);
    });

    // Call enableSubmitButton on keyup in any input field
    $('input').keyup(function () {
        enableSubmitButton();
    });

    // Call enableSubmitButton on change in any select field
    $('select').change(function () {
        enableSubmitButton();
    });

    // Initial check for form validity
    enableSubmitButton();

    // Form submission
    $("#form").submit(function (event) {
        // Validate the date range again before form submission
        if (!validateDateRange()) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });

    // Function to validate the Course Name field
    function validatecourse_name() {
        const name = $("#course_name").val();
        const lettersWithSpaces = /^[A-Za-z\s]+$/;
        if (name.trim() === "") {
            displayErrorMessage("#course_name", "Enter the Course Name");
        } else if (name.length < 5) {
            displayErrorMessage("#course_name", "Course Name should be at least 5 characters");
        } else if (!lettersWithSpaces.test(name)) {
            displayErrorMessage("#course_name", "Enter alphabets only as course name");
        } else {
            $("#course_namespan").html("");
        }
    }

    // Function to validate the Course Mode field
    function validatecourse_mode() {
        const name = $("#course_mode").val();
        if (name.trim() === "") {
            displayErrorMessage("#course_mode", "Select the Course Mode");
        } else {
            $("#course_modespan").html("");
        }
    }

    // Function to validate the Course Type field
    function validatecourse_type() {
        const name = $("#course_type").val();
        if (name.trim() === "") {
            displayErrorMessage("#course_type", "Choose the course type");
        } else {
            $("#course_typespan").html("");
        }
    }

    // Function to validate the Academic Disciplines field
    function validateacademic_disciplines() {
        const name = $("#academic_disciplines").val();
        if (name.trim() === "") {
            displayErrorMessage("#academic_disciplines", "Choose the course Discipline");
        } else {
            $("#academic_disciplinesspan").html("");
        }
    }

    // Function to validate the Course Description field
    function validatecourse_desc() {
        const description = $("#course_desc").val();
        if (description.trim() === "") {
            displayErrorMessage("#course_desc", "Enter the course description");
        } else if (description.length < 10) {
            displayErrorMessage("#course_desc", "Description should be at least 10 characters");
        } else if (description.length > 1000) {
            displayErrorMessage("#course_desc", "Description should not exceed 1000 characters");
        } else {
            $("#course_descspan").html("");
        }
    }

    // Function to validate the Eligibility field
    function validateeligibility() {
        const eligibilityCriteria = $("#eligibility").val();
        if (eligibilityCriteria.trim() === "") {
            displayErrorMessage("#eligibility", "Enter the eligibility criteria");
        } else if (eligibilityCriteria.length < 10) {
            displayErrorMessage("#eligibility", "Eligibility criteria should be at least 10 characters");
        } else if (eligibilityCriteria.length > 5000) {
            displayErrorMessage("#eligibility", "Eligibility criteria should not exceed 5000 characters");
        } else {
            $("#eligibilityspan").html("");
        }
    }

    // Function to validate the Fees field
    function validatefees() {
        const feesInput = $("#fees").val();
        if (feesInput.trim() === "") {
            displayErrorMessage("#fees", "Enter the Course fee per semester");
        } else if (parseFloat(feesInput) < 0) {
            displayErrorMessage("#fees", "Course fee cannot be a negative number");
        } else {
            $("#feesspan").html("");
        }
    }

    // Function to validate the Duration field
    function validateduration() {
        const name = $("#duration").val();
        if (name.trim() === "") {
            displayErrorMessage("#duration", "Enter the course duration");
        } else {
            $("#durationspan").html("");
        }
    }

    // Function to validate the Opening Date field
    function validateopendate() {
        const name = $("#opendate").val();
        if (name.trim() === "") {
            displayErrorMessage("#opendate", "Pick the application opening date");
        } else {
            $("#opendatespan").html("");
        }
    }

    // Function to validate the Application Deadline field
    function validateappdeadline() {
        const name = $("#appdeadline").val();
        if (name.trim() === "") {
            displayErrorMessage("#appdeadline", "Pick the application deadline");
        } else {
            $("#appdeadlinespan").html("");
        }
    }

    function validateseat_available() {
        const seatsAvailable = $("#seats_available").val();
    
        if (seatsAvailable.trim() === "") {
            displayErrorMessage("#seats_available", "Enter total Available seats");
        } else {
            const seatsAvailableValue = parseInt(seatsAvailable);
    
            if (isNaN(seatsAvailableValue) || seatsAvailableValue < 1 || seatsAvailableValue > 200 || seatsAvailableValue % 1 !== 0) {
                displayErrorMessage("#seats_available", "Enter a valid number between 1 and 200 with no decimals");
            } else {
                $("#seats_availablespan").html("");
            }
        }
    }
    
    

    // Function to validate the Thumbnail Image field
    function validatethumbnail_image() {
        const thumbnailImage = $("#thumbnail_image")[0].files[0];
        const allowedFormats = ["image/jpeg", "image/jpg", "image/png"];
    
        if (!thumbnailImage) {
            displayErrorMessage("#thumbnail_image", "Upload a thumbnail image");
        } else if (!allowedFormats.includes(thumbnailImage.type)) {
            displayErrorMessage("#thumbnail_image", "Invalid image format. Supported formats: JPEG, JPG, PNG");
        } else {
            $("#thumbnail_imagespan").html("");
        }
    
        enableSubmitButton(); 
    }

    // Function to calculate the minimum and maximum dates for opendate and appdeadline inputs
    function updateDateRange() {
        // Get the current date
        var today = new Date();
        var minOpenDate = new Date(today);
        var maxOpenDate = new Date(today);
        var minAppDeadline = new Date(today);
        var maxAppDeadline = new Date(today);

        // Calculate the minimum opendate (today + 2 days)
        minOpenDate.setDate(minOpenDate.getDate() + 2);

        // Calculate the maximum opendate (today + 2 days + 1 month)
        maxOpenDate.setDate(maxOpenDate.getDate() + 2);
        maxOpenDate.setMonth(maxOpenDate.getMonth() + 1);

        // Calculate the minimum appdeadline (opendate + 1 month)
        minAppDeadline.setMonth(minAppDeadline.getMonth() + 1);

        // Calculate the maximum appdeadline (opendate + 3 months)
        maxAppDeadline.setMonth(maxAppDeadline.getMonth() + 3);

        // Format dates in 'yyyy-mm-dd' format
        var minOpenDateStr = minOpenDate.toISOString().split('T')[0];
        var maxOpenDateStr = maxOpenDate.toISOString().split('T')[0];
        var minAppDeadlineStr = minAppDeadline.toISOString().split('T')[0];
        var maxAppDeadlineStr = maxAppDeadline.toISOString().split('T')[0];

        // Set the minimum and maximum dates for opendate and appdeadline inputs
        document.getElementById('opendate').min = minOpenDateStr;
        document.getElementById('opendate').max = maxOpenDateStr;
        document.getElementById('appdeadline').min = minAppDeadlineStr;
        document.getElementById('appdeadline').max = maxAppDeadlineStr;
    }

    // Set the initial date range
    updateDateRange();

    // Function to validate date range
    function validateDateRange() {
        var opendateInput = document.getElementById('opendate');
        var appdeadlineInput = document.getElementById('appdeadline');

        // Get the selected dates from the inputs
        var selectedOpenDate = new Date(opendateInput.value);
        var selectedAppDeadline = new Date(appdeadlineInput.value);

        // Get the minimum and maximum date range
        var minOpenDate = new Date(opendateInput.min);
        var maxOpenDate = new Date(opendateInput.max);
        var minAppDeadline = new Date(appdeadlineInput.min);
        var maxAppDeadline = new Date(appdeadlineInput.max);

        // Check if the selected dates are within the date range
        if (selectedOpenDate < minOpenDate || selectedOpenDate > maxOpenDate) {
            document.getElementById('opendatespan').textContent = 'Date must be between ' + minOpenDate.toISOString().split('T')[0] + ' and ' + maxOpenDate.toISOString().split('T')[0];
            return false;
        } else {
            document.getElementById('opendatespan').textContent = '';
        }

        if (selectedAppDeadline < minAppDeadline || selectedAppDeadline > maxAppDeadline) {
            document.getElementById('appdeadlinespan').textContent = 'Date must be between ' + minAppDeadline.toISOString().split('T')[0] + ' and ' + maxAppDeadline.toISOString().split('T')[0];
            return false;
        } else {
            document.getElementById('appdeadlinespan').textContent = '';
        }

        return true;
    }

    // Function to check the overall form validity
    function checkFormValidity() {
        // Validate all fields
        fields.forEach(field => field.validate());
        
        // Validate the date range
        validateDateRange();
        
        // Enable or disable the submit button
        enableSubmitButton();
    }
    
    // Call checkFormValidity initially
    checkFormValidity();
});
