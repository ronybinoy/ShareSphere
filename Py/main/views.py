from random import randint
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Course, Room, Message, CustomUser, Inst_info, Course_Application
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse
from django.template.defaultfilters import register
from datetime import date
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Avg


def is_migrant(user):
    return user.is_authenticated and user.is_migrant


def is_institute(user):
    return user.is_authenticated and user.is_institute


def is_staff(user):
    return user.is_authenticated and user.is_staff


# def is_landlord(user):
#     return user.is_authenticated and user.is_landlord


def login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        if request.user.is_migrant:
            # Redirect to the migrant dashboard or your desired URL for migrants
            return redirect("home")  # Replace with your URL name
        elif request.user.is_institute:
            # Redirect to the institute dashboard or your desired URL for institutes
            return redirect("institute_dashboard")  # Replace with your URL name
        # elif request.user.is_landlord:
        #     # Redirect to the landlord dashboard or your desired URL for landlords
        #     return redirect('landlord_dashboard')  # Replace with your URL name
        else:
            # Redirect to a generic home page or your desired URL
            return redirect("home")  # Replace with your URL name

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                if user.is_migrant:
                    # Redirect to the migrant dashboard or your desired URL for migrants
                    return redirect("home")  # Replace with your URL name
                elif user.is_institute:
                    # Redirect to the institute dashboard or your desired URL for institutes
                    return redirect("institute_dashboard")  # Replace with your URL name
                # elif user.is_landlord:
                #     # Redirect to the landlord dashboard or your desired URL for landlords
                #     return redirect('landlord_dashboard')  # Replace with your URL name
                else:
                    # Redirect to a generic home page or your desired URL
                    return redirect("home")  # Replace with your URL name
            else:
                error_message = "Invalid login credentials."
                return render(request, "login.html", {"error_message": error_message})
        else:
            error_message = "Please fill out all fields."
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        migrant_uid = request.POST.get("uid")
        lname = request.POST.get("lname")
        nation = request.POST.get("nation")
        password = request.POST.get("pass")
        Cpassword = request.POST.get("cpass")

        if (
            CustomUser.objects.filter(username=username).exists()
            or CustomUser.objects.filter(email=email).exists()
        ):
            messages.error(request, "Email or Username Already Exists")
            return render(request, "login.html")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password,
                nationality=nation,
                migrant_uid=migrant_uid,
                is_migrant=True,
            )
            user.save()

            return redirect("login")
    else:
        return render(request, "migrant_signup.html")


def inst_signup(request):
    if request.method == "POST":
        username = request.POST.get("email")
        email = request.POST.get("email")
        inname = request.POST.get("inname")
        institute_lis_no = request.POST.get("lno")
        nation = request.POST.get("nation")
        password = request.POST.get("pass")
        region = request.POST.get("region")  # Updated field name
        Cpassword = request.POST.get("cpass")
        print(region)  # Updated variable name

        if (
            CustomUser.objects.filter(username=username).exists()
            or CustomUser.objects.filter(email=email).exists()
        ):
            messages.error(request, "Email Already Registered")
            return render(request, "login.html")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=inname,
                email=email,
                password=password,
                institute_lis_no=institute_lis_no,
                nationality=nation,
                region=region,  # Updated field name
                is_institute=True,
            )
            user.save()

            return redirect("login")
    else:
        return render(request, "institute_signup.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        # Update first_name and last_name
        request.user.first_name = request.POST["first_name"]
        request.user.last_name = request.POST["last_name"]
        request.user.save()

        # Change password if provided
        new_password = request.POST["password"]
        if new_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password changed successfully.")

        messages.success(request, "Profile updated successfully.")
        return redirect("edit_profile")  # Redirect back to the form

    return render(request, "profile_edit.html")


@login_required
@user_passes_test(is_institute)
def addcourse(request):
    if request.method == "POST":
        user = request.user

        # Get form data
        course_name = request.POST.get("course_name")
        course_mode = request.POST.get("course_mode")
        course_type = request.POST.get("course_type")
        course_desc = request.POST.get("course_desc")
        academic_disciplines = request.POST.get("academic_disciplines")
        eligibility = request.POST.get("eligibility")
        duration = request.POST.get("duration")
        fees = request.POST.get("fees")
        appdeadline = request.POST.get("appdeadline")
        opendate = request.POST.get("opendate")
        seat_available = request.POST.get("seats_available")

        # Handle image upload
        thumbnail_image = request.FILES.get("thumbnail_image")

        # Check if the uploaded file is an image
        if thumbnail_image:
            if not thumbnail_image.content_type.startswith("image"):
                raise ValidationError("Uploaded file is not an image.")
            else:
                # If it's an image, create a Course instance and save it
                course = Course(
                    user=user,
                    course_name=course_name,
                    course_type=course_type,
                    course_mode=course_mode,
                    academic_disciplines=academic_disciplines,
                    course_desc=course_desc,
                    eligibility=eligibility,
                    duration=duration,
                    fees=fees,
                    appdeadline=appdeadline,
                    opendate=opendate,
                    is_active=True,
                    thumbnail_image=thumbnail_image,
                    seat_available=seat_available,
                )
                course.save()
        else:
            # Handle the case where no image was uploaded
            course = Course(
                user=user,
                course_name=course_name,
                course_type=course_type,
                course_mode=course_mode,
                academic_disciplines=academic_disciplines,
                course_desc=course_desc,
                eligibility=eligibility,
                duration=duration,
                fees=fees,
                appdeadline=appdeadline,
                opendate=opendate,
                seat_available=seat_available,
                is_active=True,
            )
            course.save()

        # Redirect to the dashboard or another page
        return redirect("institute_dashboard")

    return render(request, "addcourse.html")


@login_required
@user_passes_test(is_institute)
def editcourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        # Retrieve the updated data from the form fields
        course.course_name = request.POST.get("course_name")
        course.course_mode = request.POST.get("course_mode")
        course.course_type = request.POST.get("course_type")
        course.academic_disciplines = request.POST.get("academic_disciplines")
        course.eligibility = request.POST.get("eligibility")
        course.course_desc = request.POST.get("course_desc")
        course.duration = request.POST.get("duration")
        course.fees = request.POST.get("fees")
        course.appdeadline = request.POST.get("appdeadline")
        course.opendate = request.POST.get("opendate")
        course.seat_available = request.POST.get("seats_available")

        # Check if a new thumbnail image was uploaded
        new_thumbnail_image = request.FILES.get("thumbnail_image")

        seat_available = request.POST.get("seat_available")
        if seat_available is not None:
            course.seat_available = seat_available

        if new_thumbnail_image:
            # Check if the uploaded file is an image
            if not new_thumbnail_image.content_type.startswith("image"):
                raise ValidationError("Uploaded file is not an image.")

            # Update the course's thumbnail image
            course.thumbnail_image = new_thumbnail_image

        course.status = "pending"

        # Save the updated course
        course.save()
        
        return redirect("courselisting")

    return render(request, "editcourse.html", {"course": course})


@login_required
@user_passes_test(is_institute)
def deletecourse(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        # Set the course status to inactive
        course.is_active = False
        course.save()
        # Optionally, you can add a success message here
    except Course.DoesNotExist:
        # Handle the case where the course doesn't exist
        pass
    return redirect("courselisting")


# views.py

@login_required
def validate_institute(request):
    if request.method == "POST":
        license_number = request.POST.get("license_number")
        inst_email = request.POST.get("inst_email")

        # Use Django's ORM to query the Inst_info table
        try:
            institute = Inst_info.objects.get(
                license_number=license_number, inst_email=inst_email
            )
            verified = True
        except Inst_info.DoesNotExist:
            verified = False

        data = {"verified": verified}
        return JsonResponse(data)


def home(request):
    return render(request, "home.html")


@login_required
@user_passes_test(is_institute)
def institute_dashboard(request):
    return render(request, "inst_home.html")


@login_required
@user_passes_test(is_institute)
def courselisting(request):
    user = request.user
    courses = Course.objects.filter(user=user)
    current_date = timezone.now().date()

    # Create a list of tuples, each containing a course and a boolean indicating whether to disable the buttons
    course_list = []
    for course in courses:
        is_disabled = course.opendate < current_date
        course_list.append((course, is_disabled))

    return render(request, "courselisting.html", {"courses": course_list})

@login_required
def education(request):
    return render(request, "index.html")


def loggout(request):
    logout(request)
    return redirect("home")


def chatapp(request):
    return render(request, "chatroom/frontpage.html")


@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, "chatroom/rooms.html", {"rooms": rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room).order_by("date_added")[:1000]
    return render(request, "chatroom/room.html", {"room": room, "messages": messages})


@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, "admin/admin_index.html", {"users": users})


@login_required
def user_listing(request):
    return render(request, "http://127.0.0.1:8000/admin/main/customuser/")


@login_required
def filtered_users(request, role):
    if role == "all":
        users = CustomUser.objects.all()
    elif role == "migrant":
        users = CustomUser.objects.filter(is_migrant=True)
    elif role == "institute":
        users = CustomUser.objects.filter(is_institute=True)
    else:
        users = []

    user_data = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined.strftime("%Y/%m/%d"),
            "is_active": user.is_active,
            "email": user.email,
            "is_migrant": user.is_migrant,
            "is_institute": user.is_institute,
        }
        for user in users
    ]

    return JsonResponse({"users": user_data})


@login_required
def course_listing(request):
    # Retrieve pending courses with related user data
    courses = Course.objects.filter(status="pending").select_related("user")

    # Serialize the courses data including user data
    serialized_courses = [
        {
            "id": course.id,
            "course_name": course.course_name,
            "course_mode": course.course_mode,
            "course_type": course.course_type,
            "eligibility": course.eligibility,
            "duration": course.duration,
            "fees": course.fees,
            "user": {
                "first_name": course.user.first_name,
                # Add other user fields if needed
            },
            'thumbnail_image_url': course.thumbnail_image.url, 
            
        }
        for course in courses
    ]

    # Return the JSON response with courses data
    return JsonResponse({"courses": serialized_courses})


@login_required
def course_view(request, course_type):
    today = date.today()  # Get the current date
    courses_list = Course.objects.filter(
        status="approved", course_type=course_type, appdeadline__gte=today
    )
    
    # Number of courses to display per page
    per_page = 10

    paginator = Paginator(courses_list, per_page)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    return render(request, "courseview.html", {"courses": courses, "today": today})

@login_required
@require_GET
def update_course_status(request, course_id, status):
    # Get the course instance
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is still pending before updating the status
    if course.status == "pending":
        # Update the status
        course.status = status
        course.save()

        # You can also perform other actions here if needed

        return JsonResponse({"success": True, "message": "Status updated successfully"})

    return JsonResponse({"success": False, "message": "Course is no longer pending"})



@login_required
def reject_course(request, course_id):
    if request.method == 'POST':
        try:
            remarks = request.POST.get('remarks')  # Get the remarks from the POST data
            course = Course.objects.get(id=course_id)

            # Update the course status and add remarks
            course.status = 'rejected'
            print(remarks)
            course.rejection_remark = remarks
            course.save()

            # You can also perform other actions as needed

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def search_courses(request):   
    keyword = request.GET.get("keyword", "")


    # Perform the search using a Q object to filter the Course model
    courses = Course.objects.filter(
        Q(course_name__icontains=keyword)
        | Q(user__first_name__icontains=keyword)
        | Q(course_type__icontains=keyword)
    )

    # Serialize the results to JSON
    serialized_results = []

    if courses.exists():
        for course in courses:
            serialized_results.append(
                {
                    "id": course.id,
                    "course_name": course.course_name,
                    "user_first_name": course.user.first_name,
                    "course_type": course.course_type,
                    "thumbnail_image": course.thumbnail_image.url,
                    "appdeadline": course.appdeadline,
                    "course_mode": course.course_mode,
                    "college_location": course.user.region,
                }
            )
    else:
        print("No results found.")

    return JsonResponse({"courses": serialized_results})


@login_required
def get_institute_name(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")  # Get the user ID from the AJAX request
        try:
            user = CustomUser.objects.get(id=user_id)
            institute_name = (
                user.first_name
            )  # Assuming first_name contains the institute name
            return JsonResponse({"institute_name": institute_name})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
@register.filter
def course_already_applied(course, user):
    return Course_Application.objects.filter(course=course, user=user).exists()


@login_required
def generate_unique_application_id():
    while True:
        # Generate a random 7-digit ID
        application_id = randint(1000000, 9999999)
        # Check if the generated ID already exists in the database
        if not Course_Application.objects.filter(application_id=application_id).exists():
            return application_id

@login_required
def application_form(request):
    if request.method == "POST":
        user = request.user
        course_name = request.POST["course_name"]

        # Check if the user has already applied for this course
        if Course_Application.objects.filter(
            course__course_name=course_name, user=user
        ).exists():
            return HttpResponse("You have already applied for this course.")

        # Generate a unique 7-digit application ID
        application_id = generate_unique_application_id()

        full_name = request.POST["fullName"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        date_of_birth = request.POST["dateOfBirth"]
        citizenship = request.POST["citizenship"]
        country = request.POST["country"]
        province = request.POST["province"]
        street_address1 = request.POST["streetAddress1"]
        street_address2 = request.POST["streetAddress2"]
        postal_code = request.POST["postalCode"]
        contact_number = request.POST["contactNumber"]
        qualification1 = request.POST["qualification1"]
        institute1 = request.POST["institute1"]
        percentage1 = Decimal(request.POST["percentage1"])  # Convert to Decimal
        passing_year1 = int(request.POST["passingYear1"])
        english_proficiency_test = request.POST["englishProficiencyTest"]
        english_score = Decimal(request.POST["englishScore"])  # Convert to Decimal
        english_validity = request.POST["englishValidity"]
        proficiency_result = request.FILES.get("proficiencyResult")
        policy_declaration = request.POST.get("policyDeclaration") == "on"

        # Calculate the average percentage
        ielts_max_score = Decimal('9.0')  # Maximum score for IELTS
        toefl_max_score = Decimal('120.0')  # Maximum score for TOEFL

        if english_proficiency_test == "ielts":
            english_percentage = (english_score / ielts_max_score) * Decimal('100.0')
        elif english_proficiency_test == "toefl":
            english_percentage = (english_score / toefl_max_score) * Decimal('100.0')
        else:
            english_percentage = Decimal('0.0')  # Set a default value if no test is selected

        average_percentage = (english_percentage + percentage1) / Decimal('2.0')

        # Create and save the Course_Application instance
        try:
            course = Course.objects.get(course_name=course_name)
        except Course.DoesNotExist:
            return HttpResponse(f'Course "{course_name}" does not exist.')

        application_date = timezone.now().date()
        applicant = Course_Application(
            application_id=application_id,
            user=user,
            course=course,
            full_name=full_name,
            email=email,
            gender=gender,
            date_of_birth=date_of_birth,
            citizenship=citizenship,
            country=country,
            province=province,
            street_address1=street_address1,
            street_address2=street_address2,
            postal_code=postal_code,
            contact_number=contact_number,
            qualification1=qualification1,
            institute1=institute1,
            percentage1=percentage1,
            passing_year1=passing_year1,
            english_proficiency_test=english_proficiency_test,
            english_score=english_score,
            english_validity=english_validity,
            proficiency_result=proficiency_result,
            policy_declaration=policy_declaration,
            average_percentage=average_percentage,
            application_date=application_date
        )
        

        applicant.save()

        if course.course_type == "Diploma Programme":
            return redirect(reverse('course_view_diploma'))
        elif course.course_type == "Bachelor Degree":
            return redirect(reverse('course_view_bachelor'))
        elif course.course_type == "Master Degree":
            return redirect(reverse('course_view_master'))

    return render(request, "courseview.html")

@login_required
def display_applications(request):
    # Retrieve the user's applications
    user_applications = Course_Application.objects.filter(user=request.user)

    return render(request, 'viewapplication.html', {'user_applications': user_applications})

@login_required
@user_passes_test(is_institute)
def manage_applications(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id, user=user)

    # Get the number of available seats for the course
    available_seats = course.seat_available

    # Get all applications for the course ordered by average_percentage in descending order
    all_applications = Course_Application.objects.filter(course=course).order_by('-average_percentage')

    # Separate approved, pending, and rejected applications
    approved_applications = all_applications[:available_seats]
    pending_applications = all_applications[available_seats:available_seats + 2]
    rejected_applications = all_applications[available_seats + 2:]

    return render(request, "manage_applications.html", {
        "course": course,
        "all_applications": all_applications,  # Add this line
        "approved_applications": approved_applications,
        "pending_applications": pending_applications,
        "rejected_applications": rejected_applications
    })


@login_required
def send_emails(request, course_id):
    if request.method == 'POST':
        selected_application_ids = request.POST.getlist('selected_applications')
        print(selected_application_ids)
        
        # Get the approved applications
        approved_applications = Course_Application.objects.filter(pk__in=selected_application_ids)
        
        # Compose and send email for each approved application
        subject = 'Course Application Approved'
        from_email = 'sharesphereedu@gmail.com'  # Use your sender email address

        for application in approved_applications:
            recipient_email = application.email
            message = f'Congratulations! Your course application for the {application.course.course_name} at {application.user.first_name}, {application.user.region} has been approved.'
            send_mail(subject, message, from_email, [recipient_email])

        # Redirect to the 'manage_applications' view with the course_id argument
        return redirect(reverse('manage_applications', args=[course_id]))

    return JsonResponse({'message': 'Invalid request method'})


def course_application_analytics(request):
    # Calculate the total number of course applications
    total_applications = Course_Application.objects.count()

    # Find the most applied course
    most_applied_course = Course_Application.objects.values('course__course_name').annotate(application_count=Count('application_id')).order_by('-application_count').first()

    # Calculate the average percentage of applicants
    average_percentage = Course_Application.objects.aggregate(avg_percentage=Avg('average_percentage'))['avg_percentage']

    # Count the number of applicants from each country
    countries = Course_Application.objects.values('country').annotate(count=Count('application_id'))

    return render(request, 'analytics.html', {
        'total_applications': total_applications,
        'most_applied_course': most_applied_course,
        'average_percentage': average_percentage,
        'countries': {entry['country']: entry['count'] for entry in countries},
    })