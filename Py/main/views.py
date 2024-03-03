import datetime
from random import randint
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from .models import (
    Course,
    Room,
    Message,
    CustomUser,
    Inst_info,
    Course_Application,
    Migrant,
    Payment,
    Property,
    Landlord,
    Accbooking,
)
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse
from django.template.defaultfilters import register
from datetime import date
from datetime import datetime as datetime_module
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.core.files.storage import default_storage
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
import pdfkit
from django.template.loader import get_template
from django.http import HttpResponse


User = get_user_model()


def is_migrant(user):
    return user.is_authenticated and user.is_migrant


def is_institute(user):
    return user.is_authenticated and user.is_institute


def is_staff(user):
    return user.is_authenticated and user.is_staff


def is_landlord(user):    
    return user.is_authenticated and user.is_landlord


def login(request):
    
    if request.user.is_authenticated:
        if request.user.is_migrant:
            # Redirect to the migrant dashboard or your desired URL for migrants
            print("migrant")
            return redirect("home")  # Replace with your URL name
        elif request.user.is_institute:
            # Redirect to the institute dashboard or your desired URL for institutes
            return redirect("institute_dashboard")  # Replace with your URL name
        # Replace with your URL name
        elif request.user.id != AnonymousUser.id:
            print("anon")
            return redirect("home")

        else:
            # Redirect to a generic home page or your desired URL
            print("else")
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
                
                elif request.user.is_landlord:
                    return redirect("acc_home")
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
                region=region,  
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
        course_code = request.POST.get("course_code")

        # Course code validation
        if Course.objects.filter(course_code=course_code).exists():
            return JsonResponse({"error": "Course code already exists."})

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
                    course_code=course_code,  # Set the course_code
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
                course_code=course_code,  # Set the course_code
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
    user = request.user
    profile_photo_url = None  # Initialize as None, in case there's no profile photo

    # Check if the user is authenticated (not an AnonymousUser)
    if not isinstance(user, AnonymousUser):
        # Check if the user has a migrant profile
        migrant, created = Migrant.objects.get_or_create(user=user)

        if request.method == "POST":
            # Update user profile fields
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()

            # Check if the user has a migrant profile
            if migrant.dob is None:  # Check if dob is empty in the database
                dob = request.POST.get("dob")
                if dob:
                    migrant.dob = dob

            migrant.contact_no = request.POST.get("contact_no")

            # Handle profile photo update
            profile_photo = request.FILES.get("profile_photo")
            if profile_photo:
                # Delete the old profile photo if it exists
                if migrant.profile_photo:
                    default_storage.delete(migrant.profile_photo.name)
                # Save the new profile photo
                migrant.profile_photo = profile_photo

            migrant.save()

            # Redirect to a success page or reload the current page
            return redirect("home")

        # Retrieve the current profile photo URL
        if migrant.profile_photo:
            profile_photo_url = migrant.profile_photo.url

    return render(
        request, "home.html", {"user": user, "profile_photo_url": profile_photo_url}
    )


@login_required
@user_passes_test(is_institute)
def institute_dashboard(request):
    return render(request, "inst_home.html")


@login_required
@user_passes_test(is_institute)
def courselisting(request):
    user = request.user

    # Count the active courses posted by the current user
    active_count = Course.objects.filter(user=user, is_active=True).count()

    # Retrieve all courses posted by the current user
    courses = Course.objects.filter(user=user)
    current_date = date.today()  # Get the current date

    # Create a list of dictionaries, each containing course information
    course_list = []

    for course in courses:
        is_disabled = course.opendate <= current_date
        course_data = {
            "course": course,
            "is_disabled": is_disabled,
            "today": current_date,  # Include today's date in the course data
        }
        course_list.append(course_data)

    return render(
        request,
        "courselisting.html",
        {"courses": course_list, "active_count": active_count},
    )


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
    rooms = Room.objects.filter(is_active=True)  # Filter rooms with is_active=True
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

    # Fetch room names and message counts using an annotation
    room_data = Room.objects.all().annotate(message_count=Count("messages"))

    return render(
        request, "admin/admin_index.html", {"users": users, "room_data": room_data}
    )


@login_required
@user_passes_test(is_staff)
def update_user_status(request, user_id):
    if request.method == "POST":
        try:
            user = CustomUser.objects.get(id=user_id)
            new_status = request.POST.get("status")

            if new_status == "active" and not user.is_active:
                user.is_active = True
                send_mail(
                    "Your Sharesphere Account is Reactivated",
                    "Your Sharesphere account has been reactivated. Email to sharesphereedu@gmail.com for more details ",
                    "sharesphereedu@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
            elif new_status == "inactive" and user.is_active:
                user.is_active = False
                send_mail(
                    "Your Sharesphere Account is Deactivated",
                    "Your Sharesphere account has been deactivated. Email to sharesphereedu@gmail.com for more details",
                    "sharesphereedu@gmail.com",
                    [user.email],
                    fail_silently=False,
                )

            user.save()
            return JsonResponse({"success": True})
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"})
    return JsonResponse({"success": False, "message": "Invalid request"})


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


# for admin dashboard
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
            "thumbnail_image_url": course.thumbnail_image.url,
        }
        for course in courses
    ]

    # Return the JSON response with courses data
    return JsonResponse({"courses": serialized_courses})

@login_required
def course_view(request, course_type):
    today = date.today()
    query = request.GET.get("q")
    country_filter = request.GET.get("country")

    # Query the courses
    courses_list = Course.objects.filter(
        status="approved", course_type=course_type, appdeadline__gte=today
    ).select_related("user")

    # Apply search query
    if query:
        courses_list = courses_list.filter(
            Q(course_name__icontains=query) | Q(user__first_name__icontains=query)
        )

    # Apply country filter if specified
    if country_filter:
        courses_list = courses_list.filter(user__nationality=country_filter)

    # Sort courses by application deadline
    courses_list = courses_list.order_by("appdeadline")

    # Check if the user has already applied to each course and add a flag to the course object
    for course in courses_list:
        
        course.already_applied = has_applied_to_course(request.user, course)

    # Group courses by country
    courses_by_country = {}
    for course in courses_list:
        country = course.user.nationality
        if country not in courses_by_country:
            courses_by_country[country] = []
        courses_by_country[country].append(course)

    # Pagination
    per_page = 10
    for country, country_courses in courses_by_country.items():
        paginator = Paginator(country_courses, per_page)
        page_number = request.GET.get("page")
        country_courses_paginated = paginator.get_page(page_number)
        courses_by_country[country] = country_courses_paginated

    # You can fetch a list of unique countries for the filter
    unique_countries = Course.objects.values_list("user__nationality", flat=True).distinct()

    context = {
        "courses_by_country": courses_by_country,
        "today": today,
        "query": query,
        "country_filter": country_filter,
        "unique_countries": unique_countries,
    }

    return render(request, "courseview.html", context)


def has_applied_to_course(user, course):
    return Course_Application.objects.filter(user=user, course=course).exists()




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
    if request.method == "POST":
        try:
            remarks = request.POST.get("remarks")  # Get the remarks from the POST data
            course = Course.objects.get(id=course_id)

            # Update the course status and add remarks
            course.status = "rejected"
            print(remarks)
            course.rejection_remark = remarks
            course.save()

            # You can also perform other actions as needed

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method"})


@login_required
def search_courses(request):
    keyword = request.GET.get("keyword", "").strip()  # Remove leading/trailing whitespace

    if not keyword:
        return JsonResponse({"courses": []})  # Return an empty list if no keyword is provided

    # Perform the search using a Q object to filter the Course model
    courses = Course.objects.filter(
        Q(course_name__icontains=keyword) |
        Q(user__first_name__icontains=keyword) |
        Q(course_type__icontains=keyword)  # Add more fields as needed
    ).filter(status='approved')  # Filter courses with status = 'approved'

    # Get the user to check which courses they have applied for
    user = request.user

    # Serialize the results to JSON
    serialized_results = []

    if courses.exists():
        for course in courses:
            # Check if the user has applied to this course
            has_applied = Course_Application.objects.filter(user=user, course=course).exists()

            # Only include the course in the results if the user has not applied
            if not has_applied:
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
def generate_unique_application_id(request):
    while True:
        # Generate a random 7-digit ID
        application_id = randint(1000000, 9999999)
        # Check if the generated ID already exists in the database
        if not Course_Application.objects.filter(
            application_id=application_id
        ).exists():
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
        application_id = generate_unique_application_id(request)

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
        ielts_max_score = Decimal("9.0")  # Maximum score for IELTS
        toefl_max_score = Decimal("120.0")  # Maximum score for TOEFL

        if english_proficiency_test == "ielts":
            english_percentage = (english_score / ielts_max_score) * Decimal("100.0")
        elif english_proficiency_test == "toefl":
            english_percentage = (english_score / toefl_max_score) * Decimal("100.0")
        else:
            english_percentage = Decimal(
                "0.0"
            )  # Set a default value if no test is selected

        average_percentage = (english_percentage + percentage1) / Decimal("2.0")

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
            application_date=application_date,
        )

        applicant.save()
        payment_url = reverse("payment1", args=[application_id])
        return redirect(payment_url)


    return render(request, "courseview.html")


@login_required
def display_applications(request):
    # Retrieve the user's applications
    user_applications = Course_Application.objects.filter(user=request.user)

    return render(
        request, "viewapplication.html", {"user_applications": user_applications}
    )


@login_required
@user_passes_test(is_institute)
def manage_applications(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id, user=user)

    # Get the number of available seats for the course
    available_seats = course.seat_available

    # Get all applications for the course ordered by average_percentage in descending order
    all_applications = Course_Application.objects.filter(course=course).order_by(
        "-average_percentage"
    )

    # Separate approved, pending, and rejected applications
    approved_applications = all_applications[:available_seats]
    pending_applications = all_applications[available_seats : available_seats + 2]
    rejected_applications = all_applications[available_seats + 2 :]

    # Check if any application has a status of "applied"
    has_applied_applications = any(
        application.application_status == "applied" for application in all_applications
    )

    return render(
        request,
        "manage_applications.html",
        {
            "course": course,
            "all_applications": all_applications,
            "approved_applications": approved_applications,
            "pending_applications": pending_applications,
            "rejected_applications": rejected_applications,
            "has_applied_applications": has_applied_applications,  # Pass the flag to the template
        },
    )


@login_required
@user_passes_test(is_institute)
def generate_results(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id, user=user)

    # Get the number of available seats for the course
    available_seats = course.seat_available

    # Get all applications for the course ordered by average_percentage in descending order
    all_applications = Course_Application.objects.filter(course=course).order_by(
        "-average_percentage"
    )

    # Update application statuses
    for i, application in enumerate(all_applications):
        if i < available_seats:
            application.application_status = "approved"
        elif i < available_seats + 2:
            application.application_status = "pending"
        else:
            application.application_status = "rejected"
        application.save()

    return redirect("manage_applications", course_id=course.id)


@login_required
def send_emails(request, course_id, email_category):
    # Get the course and the user who posted the course
    print(course_id, email_category)
    course = get_object_or_404(Course, pk=course_id)
    posteduser = course.user

    # Filter applications based on the email_category
    if email_category == "all":
        applications = Course_Application.objects.filter(course=course)
    elif email_category == "approved":
        applications = Course_Application.objects.filter(
            course=course, status="approved"
        )
    elif email_category == "pending":
        applications = Course_Application.objects.filter(
            course=course, status="pending"
        )
    elif email_category == "rejected":
        applications = Course_Application.objects.filter(
            course=course, status="rejected"
        )
    else:
        # Handle invalid email_category (e.g., return an error response)
        return JsonResponse({"message": "Invalid email category"})

    # Compose and send email for each selected application
    subject = "Course Application Status"
    from_email = "sharesphereedu@gmail.com"  # Use your sender email address

    for application in applications:
        recipient_email = application.email
        status = (
            "Approved"
            if application.application_status == "approved"
            else "Pending"
            if application.application_status == "pending"
            else "Rejected"
        )
        message = f"Your course application for the {course.course_name} at {posteduser.first_name}, {posteduser.region} has been {status}."
        send_mail(subject, message, from_email, [recipient_email])

    return JsonResponse({"message": "Emails sent successfully"})


def course_application_analytics(request):
    # Calculate the total number of course applications
    total_applications = Course_Application.objects.count()
    # Find the most applied course
    most_applied_course = (
        Course_Application.objects.values("course__course_name")
        .annotate(application_count=Count("application_id"))
        .order_by("-application_count")
        .first()
    )

    # Calculate the average percentage of applicants
    average_percentage = Course_Application.objects.aggregate(
        avg_percentage=Avg("average_percentage")
    )["avg_percentage"]

    # Count the number of applicants from each country
    countries = Course_Application.objects.values("country").annotate(
        count=Count("application_id")
    )

    return render(
        request,
        "analytics.html",
        {
            "total_applications": total_applications,
            "most_applied_course": most_applied_course,
            "average_percentage": average_percentage,
            "countries": {entry["country"]: entry["count"] for entry in countries},
        },
    )


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


def payment1(request, application_id):
    currency = "INR"
    amount = 70000  # Rs. 200  <- Make sure this matches the amount you want to capture

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture="0")
    )

    # Order ID of the newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = reverse(
        "paymenthandler", args=[application_id]
    )  # Pass the application ID in the URL

    # We need to pass these details to the frontend.
    context = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_merchant_key": settings.RAZOR_KEY_ID,
        "razorpay_amount": amount,
        "currency": currency,
        "callback_url": callback_url,
    }

    return render(request, "payment1.html", context=context)


from django.template.loader import render_to_string


@csrf_exempt
def paymenthandler(request, application_id):
    if request.method == "POST":
        try:
            # get the required parameters from the post request.
            payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            # Verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                # Capture the payment
                payment_info = razorpay_client.payment.fetch(payment_id)
                amount = payment_info["amount"]
                rupees = amount / 100
                razorpay_client.payment.capture(payment_id, amount)

                # Update the status of the Course_Application to True
                application = get_object_or_404(
                    Course_Application, application_id=application_id
                )
                application.status = True
                application.save()

                # Parse the created_at_str
                created_at_ts = payment_info["created_at"]
                created_at_dt = datetime.datetime.fromtimestamp(created_at_ts)
                created_at_str = created_at_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                created_at = datetime.datetime.strptime(
                    created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                )

                # Create a Payment instance
                payment = Payment(
                    application=application,
                    payment_amount=rupees,  # Use the actual amount from the payment
                    payment_datetime=created_at,  # Use the parsed datetime
                    user=request.user,
                    payment_status="Successful",  # Set payment status to 'Successful'
                )
                payment.save()

                return render(request, "paymentsuccess.html")
            else:
                # If signature verification fails.
                return render(request, "paymentfail.html")
        except Exception as e:
            # If there is an error while processing or capturing payment, log the error for debugging.
            print(f"Error processing payment: {e}")
            return render(request, "paymentfail.html")
    else:
        # If other than POST request is made.
        return HttpResponseBadRequest()


def invoice_view(request, application_id):
    try:
        application = Course_Application.objects.get(application_id=application_id)
        payments = Payment.objects.filter(application=application)
    except Course_Application.DoesNotExist:
        application = None
        payments = None

    return render(
        request,
        "payment_receipt.html",
        {"application": application, "payments": payments},
    )


def generate_pdf(request, application_id):
    # Get the HTML template
    template = get_template("payment_receipt.html")

    try:
        application = Course_Application.objects.get(application_id=application_id)
    except Course_Application.DoesNotExist:
        application = None

    # Retrieve payment data related to the application (replace with your actual query)
    if application:
        payments = Payment.objects.filter(application=application)
    else:
        payments = None

    # Create the context dictionary
    context = {
        "application": application,
        "payments": payments,
    }
    # Render the template with the context
    html = template.render(context)

    # PDF generation options (you can customize these)
    options = {
        "page-size": "A4",
        "margin-top": "0mm",
        "margin-right": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "encoding": "UTF-8",
    }

    # Generate PDF from the HTML content
    pdf = pdfkit.from_string(html, False, options=options)

    # Create an HTTP response with the PDF content
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

    return response


# @csrf_exempt  # This decorator is used for simplicity in this example. You should use proper CSRF protection.
# def add_room(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         slug = request.POST.get("slug")

#         # Create and save the Room object
#         room = Room(name=name, slug=slug)
#         room.save()

#         # You can return a success message or JSON response
#         return JsonResponse({"message": "Room added successfully"})
#     else:
#         # Handle other HTTP methods if needed
#         return JsonResponse({"message": "Invalid request"}, status=400)


def add_room(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        slug = request.POST.get("slug")

        # Check if a room with the same slug already exists
        if Room.objects.filter(slug=slug).exists():
            error_message = "The slug name already exists. Please choose a different one."
            
            # Generate a JavaScript alert with the error message
            script = f'<script>alert("{error_message}"); window.history.back();</script>'
            return HttpResponse(script)

        # If the room with the same slug doesn't exist, save the new room
        room = Room(name=name, slug=slug)
        room.save()

        # Generate a JavaScript alert for successful room creation
        success_message = "Chat room added successfully!"
        script = f'<script>alert("{success_message}");</script>'
        return HttpResponse(script)

    return render(request, 'admin/admin_index.html')



@csrf_exempt
def toggle_room_status(request):
    # Get the room ID from the POST request
    room_id = request.POST.get("room_id")

    # Retrieve the room object
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    # Toggle the room's status (active to inactive or vice versa)
    room.is_active = not room.is_active
    room.save()

    return JsonResponse({"message": "Room status updated successfully"})


def check_slug(request):
    slug = request.GET.get('slug')
    exists = Room.objects.filter(slug=slug).exists()
    
    return JsonResponse({'exists': exists})



def application_chart_data(request):
    application_data = Course_Application.objects.all()
    application_data_json = [
        {
            'application_date': app.application_date.strftime('%Y-%m-%d'),
            'application_count': 1,  # You can modify this based on your data
        }
        for app in application_data
    ]

    return JsonResponse(application_data_json, safe=False)


def check_unique_course_code(request):
    if request.method == 'GET':
        course_code = request.GET.get('course_code', None)  # Assuming you pass the course_code as a GET parameter
        
        if course_code is not None:
            # Query the database to check if the course_code is unique
            is_unique = not Course.objects.filter(course_code=course_code).exists()

            # Return the result as JSON
            data = {'is_unique': is_unique}
            return JsonResponse(data)
        

    # Handle other cases (e.g., POST requests) or invalid input
    return JsonResponse({'is_unique': False})





#Accomodation

from django.shortcuts import render
from .models import Property


@login_required
@user_passes_test(is_landlord)
def acc_home(request):
    if request.user.is_authenticated:
        try:
            properties = Property.objects.filter(landlord=request.user)
            rejected_properties = properties.filter(status='rejected')
            inactive_properties = properties.filter(status='inactive')
            pending_properties = properties.filter(status='pending')
            active_properties = properties.filter(status='active')  # Excluding rejected and inactive properties
            return render(request, "accomodation/acc_home.html", {'properties': properties, 'rejected_properties': rejected_properties, 'inactive_properties': inactive_properties, 'active_properties': active_properties, 'pending_properties': pending_properties})
        except Landlord.DoesNotExist:
            # Handle the case where Landlord does not exist for the current user
            raise Http404("Landlord does not exist for this user.")
    else:
        return render(request, "accomodation/acc_home.html", {'properties': [], 'rejected_properties': [], 'inactive_properties': [], 'active_properties': [], 'pending_properties': []})





def get_property_details(request):
    if request.method == 'GET':
        property_id = request.GET.get('property_id')

        try:
            property_obj = get_object_or_404(Property, id=property_id)
            property_data = {
                'property_name': property_obj.property_name,
                'address': property_obj.address,
                'country': property_obj.country,
                'state_province': property_obj.state_province,
                'city':property_obj.city,
                'contact_number': property_obj.contact_number,
                'rent_per_month': str(property_obj.rent_per_month),  # Convert DecimalField to string
                'minimum_duration_of_rent': property_obj.get_minimum_duration_of_rent_display(),
                'number_of_bedrooms': property_obj.get_number_of_bedrooms_display(),
                'number_of_bathroom': property_obj.get_number_of_bathroom_display(),
                'parking_area': property_obj.parking_area,
                'cctv': property_obj.cctv,
                'heater': property_obj.heater,
                'air_conditioning': property_obj.air_conditioning,
                'power_backup': property_obj.power_backup,
                'wifi': property_obj.wifi,
                'frontview_image': property_obj.frontview_image.url,
                'living_room_image': property_obj.living_room_image.url,
                'bedroom_image': property_obj.bedroom_image.url,
                'bathroom_image': property_obj.bathroom_image.url,
                'kitchen_image': property_obj.kitchen_image.url,
                'dining_room_image': property_obj.dining_room_image.url,
                'other1_image': property_obj.other1_image.url,
                'other2_image': property_obj.bathroom_image.url,
            }
            
            return JsonResponse(property_data)
        except Property.DoesNotExist:
            return JsonResponse({'error': 'Property not found'}, status=404)




def property_submit(request):
    if request.method == 'POST':

        landlord = request.user  # Assuming you have a logged-in user
        property_name = request.POST.get('pname')
        address = request.POST.get('address')
        property_location_link = request.POST.get('mlink')
        country = request.POST.get('nation')
        state_province = request.POST.get('region')
        city = request.POST.get('city')
        frontview_image = request.FILES.get('frontview')
        living_room_image = request.FILES.get('living')
        bedroom_image = request.FILES.get('bedroom')
        bathroom_image = request.FILES.get('bathroom')
        kitchen_image = request.FILES.get('kitchen')
        dining_room_image = request.FILES.get('dining')
        other1_image = request.FILES.get('other1')
        other2_image = request.FILES.get('other2')
        contact_number = request.POST.get('contact')
        rent_per_month = request.POST.get('rent')
        sqft = request.POST.get('sqft')
        minimum_duration_of_rent = request.POST.get('duration')
        number_of_bedrooms = request.POST.get('bhk')
        number_of_bathroom = request.POST.get('bth')
        parking_area = 'Parea' in request.POST
        cctv = 'cctv' in request.POST
        heater = 'heater' in request.POST
        air_conditioning = 'ac' in request.POST
        power_backup = 'pback' in request.POST
        wifi = 'wifi' in request.POST


        
        try:
            Property.objects.create(
                landlord=landlord,
                property_name=property_name,
                address=address,
                property_location_link=property_location_link,
                country=country,
                state_province=state_province,
                city=city,
                frontview_image=frontview_image,
                living_room_image=living_room_image,
                bedroom_image=bedroom_image,
                bathroom_image=bathroom_image,
                kitchen_image=kitchen_image,
                dining_room_image=dining_room_image,
                other1_image=other1_image,
                other2_image=other2_image,
                contact_number=contact_number,
                rent_per_month=rent_per_month,
                minimum_duration_of_rent=minimum_duration_of_rent,
                number_of_bedrooms=number_of_bedrooms,
                number_of_bathroom=number_of_bathroom,
                total_squarefeet=sqft,
                parking_area=parking_area,
                cctv=cctv,
                heater=heater,
                air_conditioning=air_conditioning,
                power_backup=power_backup,
                wifi=wifi,
                status="pending"
            )
            # messages.success(request, 'Property submitted successfully!')
            return redirect('acc_home') 
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponse(status=500)

def acc_signup(request):
    if request.method == "POST":
        username = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phno")
        ccode = request.POST.get("ccode")
        uid = request.POST.get("uid")
        nation = request.POST.get("nation")
        password = request.POST.get("pass")
        cpassword = request.POST.get("cpass")
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email or Username Already Exists")
            return render(request, "login.html")
        
        else:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
                phone = phone,
                password=password,
                country_code=ccode,
                nationality=nation,
                migrant_uid=uid,
                is_landlord=True,
            )
            user.save()

            return redirect("login")
    else:
        return render(request,"accomodation/acc_signup.html")



@csrf_exempt
def pending_properties(request):
    if request.method == 'GET':
        # Retrieve pending properties with related landlord user data
        properties = Property.objects.filter(status='pending').select_related('landlord')

        # Serialize the properties data including landlord user data
        serialized_properties = [
            {
                'id': property.id,
                'property_name': property.property_name,
                'address': property.address,
                'state_province': property.state_province,
                'country': property.country,
                'contact_number': property.contact_number,
                'rent_per_month': property.rent_per_month,
                'frontview_image_url': property.frontview_image.url,
                'landlord': {
                    'first_name': property.landlord.first_name,
                    # Add other landlord user fields if needed
                },
            }
            for property in properties
        ]
        

        # Return the JSON response with properties data
        return JsonResponse({'properties': serialized_properties})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
    
    
def reject_property(request):
    if request.method == 'POST':
        property_id = request.POST.get('propertyId')
        rejection_remarks = request.POST.get('rejectRemarks')

        # Update the property status and rejection remarks
        property = Property.objects.get(id=property_id)
        property.status = 'rejected'
        property.rejection_remark = rejection_remarks
        property.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def update_property_status(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        new_status = request.POST.get('status')

        # Fetch the property and update the status
        property_instance = get_object_or_404(Property, id=property_id)

        # Debugging statement to print the current status
        print(f"Current status of property {property_instance.property_name}: {property_instance.status}")

        # Check if the property is still pending before updating the status
        # if property_instance.status == "pending":
            # Update the status
        property_instance.status = new_status
        property_instance.save()

        # You can also perform other actions here if needed

        return JsonResponse({'success': True, 'message': 'Status updated successfully'})
        # else:
        #     return JsonResponse({'success': False, 'message': 'Property is no longer pending'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def acc_userview(request):
    # Fetch only featured properties with status 'active' from the database
    featured_properties = Property.objects.filter(is_featured=True, status='active')

    context = {
        'featured_properties': featured_properties,
    }

    return render(request, "accomodation/acc_userview.html", context)


# def property_detail(request, pk):
#     property_instance = get_object_or_404(Property, pk=pk)
#     return render(request, 'accomodation/property_detail.html', {'property': property_instance})


def acc_propertyview(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        # Retrieve the property object associated with the passed ID
        property_obj = get_object_or_404(Property, id=property_id, status='active')
        return render(request, "accomodation/acc_propertyview.html", {'property': property_obj})
    else:
        # Handle the case when the request method is not POST
        return HttpResponse("Invalid request method")


def property_search(request):
    if request.method == 'GET' and 'search_query' in request.GET:
        search_query = request.GET.get('search_query')
        # Filter properties based on the search query and status
        properties = Property.objects.filter(city__icontains=search_query, status='active')
        # Serialize the properties queryset to JSON
        serialized_properties = [{
            'id': property.id,
            'property_name': property.property_name,
            'frontview_image': property.frontview_image.url,
            'rent_per_month': property.rent_per_month,
            'city': property.city,
            'state_province': property.state_province,
            'country': property.country,
        } for property in properties]
        # Return the search results as JSON response
        return JsonResponse({'properties': serialized_properties})
    else:
        return JsonResponse({'error': 'Invalid request'})
    
    
def acc_listproperty(request):
    # Fetch all active properties
    properties = Property.objects.filter(status='active')
    search_query = request.GET.get('search_query')
    
    if search_query:
        # If search query is provided, filter properties based on the city
        properties = properties.filter(Q(city__icontains=search_query))
    
    paginator = Paginator(properties, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "accomodation/acc_propertylist.html", {'page_obj': page_obj})


def edit_property_modal(request, property_id):
    # Fetch the property object based on its ID
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Pass the property object to the template
    return render(request, 'accomodation/acc_propertylist.html', {'property_obj': property_obj})


@login_required
def acc_booking(request, property_id):
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        passport_number = request.POST.get('passport_number')
        check_in_date = request.POST.get('check_in_date')
        num_adults = request.POST.get('num_adults')
        special_requests = request.POST.get('special_requests')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        emergency_contact_phone = request.POST.get('emergency_contact_phone')
        user_id = request.user.id

        # Save the data to the database and retrieve the booking ID
        booking = Accbooking.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            country=country,
            state=state,
            passport_number=passport_number,
            check_in_date=check_in_date,
            num_adults=num_adults,
            special_requests=special_requests,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_relationship=emergency_contact_relationship,
            emergency_contact_phone=emergency_contact_phone,
            user_id=user_id,
            property_id=property_id,
            is_active=False
        )
        
        # Retrieve the booking ID
        booking_id = booking.id

        # Redirect to the payment page with the booking ID
        payment_url = reverse("accpayment", args=[booking_id])
        return redirect(payment_url)

    return render(request, "accomodation/acc_booking.html", {'property_id': property_id})






razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def accpayment(request,booking_id):
    print(booking_id)
    currency = 'INR'
    amount = 200000  # Rs. 2000

    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'accpaymenthandler/'

    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'accomodation/paymentindex.html', context=context)

@csrf_exempt
def accpaymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 200000  
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'accomodation/paymentsuccess.html')
                except:
                    return render(request, 'accomodation/paymentfail.html')
            else:
                return render(request, 'accomodation/paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
    # if other than POST request is made.
        return HttpResponseBadRequest()