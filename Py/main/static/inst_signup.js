$(document).ready(function () {

    const fields = [

        { id: "#nm", validate: validateInName },
        { id: "#mail", validate: validateEmail },
        { id: "#lno", validate: validatelno },
        { id: "#pass", validate: validatePassword },
        { id: "#cpass", validate: validateConfirmPassword },
        // { id: "#nation", validate: validateNation },
        // { id: "#region", validate: validateRegion }

    ];

    fields.forEach(field => {
        $(field.id).keyup(function () {
            field.validate();
        });

        validateFieldOnBlur(field.id, field.validate);
    });

    function checkFormValidity() {
        const isValid = fields.every(field => {
            const $field = $(field.id);
            const $errorSpan = $(`${field.id}span`);

            return $field.val().trim() !== "" && $errorSpan.html() === "";
        });

        $("#submitBtn").prop("disabled", !isValid);
    }

    function validateFieldOnBlur(fieldId, validationFunction) {
        $(fieldId).blur(function () {
            validationFunction();
            checkFormValidity();
        });
    }

    // Form submission
    $("#form").submit(function (event) {
        if (!$("#submitBtn").prop("disabled")) {
            // Form is valid, allow submission
            return true;
        } else {
            // Form is not valid, prevent submission
            event.preventDefault();
            return false;
        }
    });

    // Initial check for form validity
    checkFormValidity();

    function validateInName() {
        const name = $("#nm").val();
        const lettersWithSpaces = /^[A-Za-z\s]+$/;
        if (name.trim() === "") {
            $("#nmspan").html("Enter the Institute Name").css("color", "#41586B");
        } else if (!lettersWithSpaces.test(name)) {
            $("#nmspan").html("Institute name field required only alphabet characters with spaces").css("color", "#41586B");
        } else {
            $("#nmspan").html("");
        }
    }

    function validateEmail() {
        const email = $("#mail").val();
        const filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (email === "") {
            $("#mailspan").html("Enter the Email Id").css("color", "#41586B");
        } else if (!filter.test(email)) {
            $("#mailspan").html("Use correct Email Id").css("color", "#41586B");
        } else {
            $("#mailspan").html("");
        }
    }

    function validatelno() {
        const uid = $("#lno").val();
        const filter = /^\d{12}$/;
        if (uid === "") {
            $("#lnospan").html("Enter the License number").css("color", "#41586B");
        } else if (!filter.test(uid)) {
            $("#lnospan").html("Use correct License number").css("color", "#41586B");
        } else {
            $("#lnospan").html("");
        }
    }

    
    function validatePassword() {
        const password = $("#pass").val();
        const pwd_expression = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])/;
        if (password === "") {
            $("#passspan").html("Enter the Password").css("color", "#41586B");
        } else if (!pwd_expression.test(password)) {
            $("#passspan").html("Use correct Password").css("color", "#41586B");
        } else {
            $("#passspan").html("");
        }
    }

    function validateConfirmPassword() {
        const password = $("#pass").val();
        const confirmPassword = $("#cpass").val();
        if (confirmPassword === "") {
            $("#cpassspan").html("Enter the Confirm Password").css("color", "#41586B");
        } else if (confirmPassword !== password) {
            $("#cpassspan").html("Password do not match").css("color", "#41586B");
        } else {
            $("#cpassspan").html("");
        }
    }
});

// Get references to the dropdowns
const nationDropdown = document.getElementById('nation');
const regionDropdown = document.getElementById('region');
// Define region options for each country
const countryRegions = {
    'Ireland': [
        'Connacht',
        'County Carlow',
        'County Cavan',
        'County Clare',
        'County Cork',
        'County Donegal',
        'County Dublin',
        'County Galway',
        'County Kerry',
        'County Kildare',
        'County Kilkenny',
        'County Laois',
        'County Limerick',
        'County Longford',
        'County Louth',
        'County Mayo',
        'County Meath',
        'County Monaghan',
        'County Offaly',
        'County Roscommon',
        'County Sligo',
        'County Tipperary',
        'County Waterford',
        'County Westmeath',
        'County Wexford',
        'County Wicklow',
        'Leinster',
        'Munster',
        'Ulster',
        // Add more options for Ireland as needed
    ],
    
    'Canada': [
        'Alberta',
        'British Columbia',
        'Manitoba',
        'New Brunswick',
        'Newfoundland and Labrador',
        'Northwest Territories',
        'Nova Scotia',
        'Nunavut',
        'Ontario',
        'Prince Edward Island',
        'Quebec',
        'Saskatchewan',
        'Yukon'
    ],
    // Add more countries and their regions here
};

// Function to populate the region dropdown based on the selected country
function populateRegionDropdown() {


    // Get the selected country
    const selectedCountry = nationDropdown.value;

    // Clear existing options
    regionDropdown.innerHTML = '<option value="">Select State or Province</option>';

    // Populate with options for the selected country
    if (selectedCountry in countryRegions) {
        countryRegions[selectedCountry].forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionDropdown.appendChild(option);
        });
    }

    // Show or hide the region dropdown based on the selection
    // regionDropdown.style.display = selectedCountry ? 'block' : 'none';
}

// Attach an event listener to the nation dropdown
nationDropdown.addEventListener('change', populateRegionDropdown);

// Initial population of the region dropdown based on the default selection
populateRegionDropdown();