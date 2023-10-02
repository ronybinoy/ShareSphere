from django.urls import include, path
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    path("chatroom", views.chatapp, name='chatapp'),
    path("login/", views.login, name="login"),  # Keep the login URL
    path("signup/", views.signup, name="signup"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    
    #admin
    path('user_listing/', views.user_listing, name='user_listing'),
    path('filtered_users/<str:role>/', views.filtered_users, name='filtered_users'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pending_courses/', views.course_listing, name='pending_courses'),
    path('update_course_status/<int:course_id>/<str:status>/', views.update_course_status, name='update_course_status'),


    path('payment1/', views.payment1, name='payment1'), 
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),  # Define the URL pattern for paymenthandler view
    
    path('institute-dashboard/', views.institute_dashboard, name='institute_dashboard'),
    path('manage_applications/<int:course_id>/', views.manage_applications, name='manage_applications'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('courses/diploma/', views.course_view, {'course_type': 'Diploma Programme'}, name='course_view_diploma'),
    path('courses/bachelor/', views.course_view, {'course_type': 'Bachelor Degree'}, name='course_view_bachelor'),
    path('courses/master/', views.course_view, {'course_type': 'Master Degree'}, name='course_view_master'),
    path('get_institute_name/', views.get_institute_name, name='get_institute_name'),



    path('application_form/', views.application_form, name='application_form'),
    path('user/display_applications/', views.display_applications, name='display_applications'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('course_application_analytics/', views.course_application_analytics, name='course_application_analytics'),

    

    path('courselisting/', views.courselisting, name='courselisting'),
    path('editcourse/<int:course_id>/', views.editcourse, name='editcourse'),
    path('deletecourse/<int:course_id>/', views.deletecourse, name='deletecourse'),
    path('reject_course/<int:course_id>/', views.reject_course, name='reject_course'),
    path('send_emails/<int:course_id>/', views.send_emails, name='send_emails'),



    path("inst_signup/", views.inst_signup, name="inst_signup"),
    path('validate_institute/', views.validate_institute, name='validate_institute'),
    path("education/", views.education, name="education"),
    

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),  
    path("auth/", include("social_django.urls", namespace="social")),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(  
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    path('rooms', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    
    
    
  
]
