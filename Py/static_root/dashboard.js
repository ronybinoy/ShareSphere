document.addEventListener("DOMContentLoaded", function () {
    const userListTable = document.getElementById("user-list-table");
    const roleFilter = document.getElementById("role-filter");

    roleFilter.addEventListener("change", function () {
        const selectedRole = roleFilter.value;

        // Make an AJAX request to the filtered_users view
        fetch(`/filtered_users/${selectedRole}/`)
            .then(response => response.json())
            .then(data => {
                const users = data.users;

                // Loop through the table rows and update the table
                const rows = userListTable.getElementsByTagName("tr");
                for (let i = 1; i < rows.length; i++) {
                    const row = rows[i];
                    const userId = parseInt(row.cells[0].textContent);

                    // Check if the user ID exists in the received data
                    const user = users.find(u => u.id === userId);
                    if (user) {
                        row.style.display = ""; // Show the row
                    } else {
                        row.style.display = "none"; // Hide the row
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});


// Function to update the status of a course in the database
function updateCourseStatus(courseId, status) {
    // Make an AJAX request to update the course status
    $.ajax({
        url: `/update_course_status/${courseId}/${status}/`, // Replace with the actual URL
        type: 'GET',
        dataType: 'json', // Specify JSON dataType
        success: function (data) {
            // Check if the status was updated successfully
            if (data.success) {
                // Remove the course card from the listing if it's no longer pending
                if (status !== 'pending') {
                    // Find the course card by course ID and remove it
                    $(`#course-card-${courseId}`).remove();
                }
            } else {
                console.error('Error updating course status:', data.message);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

// Function to load and display course details
function renderCourseDataToHTML(courses) {
    const container = $('#course-listing-content');

    // Clear any existing content inside the container
    container.empty();

    if (courses.length > 0) {
        // Create a new row div for every 3 cards
        let rowDiv;
        courses.forEach((course, index) => {
            if (index % 3 === 0) {
                // Start a new row for every 3 cards
                rowDiv = $('<div>').addClass('row custom-margin-row');
            }

            // Create a course card template
            const courseCard = $('<div>')
                .addClass('col-lg-4 col-md-6 col-sm-12 mb-4')
                .attr('id', `course-card-${course.id}`); // Add unique ID to the course card

            const cardDiv = $('<div>').addClass('card course-card rounded-xl');
            const cardBodyDiv = $('<div>').addClass('card-body'); // Removed 'text-center'

            const button = $('<button>')
                .addClass('btn btn-warning mb-3')
                .prop('disabled', true)
                .text('Pending');

            const courseTitle = $('<h5>')
                .addClass('card-title')
                .text(course.course_name);

            const courseMode = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Course Mode:</strong> ${course.course_mode}`);

            const courseType = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Course Type:</strong> ${course.course_type}`);

            const eligibility = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Eligibility:</strong> ${course.eligibility}`);

            const duration = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Duration:</strong> ${course.duration}`);

            const fees = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Fees per Semester:</strong> $${course.fees}`);

            const instituteName = $('<p>')
                .addClass('card-text mb-2') // Added 'mb-2' for spacing
                .html(`<strong>Institute Name:</strong> ${course.user.first_name}`);

            const approvalButton = $('<button>')
                .addClass('btn btn-success')
                .text('Approve')
                .on('click', function () {
                    updateCourseStatus(course.id, 'approved'); // Call the updateCourseStatus function with 'approved'
                });

            const rejectionButton = $('<button>')
                .addClass('btn btn-danger ms-2')
                .text('Reject')
                .on('click', function () {
                    updateCourseStatus(course.id, 'rejected'); // Call the updateCourseStatus function with 'rejected'
                });

            // Append elements to the card
            cardBodyDiv.append(
                button,
                courseTitle,
                $('<hr>'),
                courseMode,
                courseType,
                eligibility,
                duration,
                fees,
                instituteName,
                $('<div>').append(approvalButton, rejectionButton) // Removed 'text-center'
            );
            cardDiv.append(cardBodyDiv);
            courseCard.append(cardDiv);

            // Append the course card to the current row
            rowDiv.append(courseCard);

            if ((index + 1) % 3 === 0 || index === courses.length - 1) {
                // If we've added 3 cards or reached the end of the list, append the row to the container
                container.append(rowDiv);
            }
        });
    } else {
        // Display a message if there are no pending courses
        const message = $('<p>').addClass('text-white').text('There are no pending courses.');
        container.append(message);
    }
}

function loadCourseDetails() {
    $.ajax({
        url: '/pending_courses/', // Replace with the actual URL
        type: 'GET',
        dataType: 'json', // Specify JSON dataType
        success: function (data) {
            try {
                // Assuming the server sends a JSON array of course objects
                if (Array.isArray(data.courses)) {
                    renderCourseDataToHTML(data.courses);
                    $('#course-listing-content').show();
                    $('#users-content').hide();
                } else {
                    console.error('Invalid JSON response:', data);
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}


$(document).ready(function () {
    $('#users-content').show();
    $('#course-listing-content').hide();

    // Add click event listeners to the buttons in the sidebar
    $('.show-users-btn').click(function () {
        $('#users-content').show();
        $('#course-listing-content').hide();
    });

    $('.show-course-listing-btn').click(function () {
        loadCourseDetails(); // Fetch and display pending courses
        $('#users-content').hide();
        $('#course-listing-content').show();
    });
});
