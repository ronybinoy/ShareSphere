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
    path('add_room/', views.add_room, name='add_room'),
    path('check-slug/', views.check_slug, name='check-slug'),
    path('toggle_room_status/', views.toggle_room_status, name='toggle_room_status'),
    path('update_user_status/<int:user_id>/', views.update_user_status, name='update_user_status'),
    path('pending_courses/', views.course_listing, name='pending_courses'),
    path('update_course_status/<int:course_id>/<str:status>/', views.update_course_status, name='update_course_status'),



    path('payment1/<int:application_id>/', views.payment1, name='payment1'),
    path('paymenthandler/<int:application_id>/', views.paymenthandler, name='paymenthandler'),
    path('invoice/<str:application_id>/', views.invoice_view, name='invoice'),
    path('generate_pdf/<int:application_id>/', views.generate_pdf, name='generate_pdf'),




    
    path('institute-dashboard/', views.institute_dashboard, name='institute_dashboard'),
    path('manage_applications/<int:course_id>/', views.manage_applications, name='manage_applications'),
    path('check_unique_course_code/', views.check_unique_course_code, name='check_unique_course_code'),
    path('addcourse/', views.addcourse, name='addcourse'),
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
    path('send_emails/<int:course_id>/<str:email_category>/', views.send_emails, name='send_emails'),
    path('generate_results/<int:course_id>/', views.generate_results, name='generate_results'),

    path('application_chart_data/', views.application_chart_data, name='application_chart_data'),




    path("inst_signup/", views.inst_signup, name="inst_signup"),
    path('validate_institute/', views.validate_institute, name='validate_institute'),
    path("education/", views.education, name="education"),
    
    
    
    
    path("acc_signup/", views.acc_signup, name="acc_signup"),
    path("acc_home/", views.acc_home, name="acc_home"),
    path("property_submit/", views.property_submit, name="property_submit"),
    path("property_submit", views.property_submit),
    path('get_property_details/', views.get_property_details, name='get_property_details'),
    path('pending_properties/', views.pending_properties, name='pending_properties'),
    path('reject_property/', views.reject_property, name='reject_property'),
    path('update_property_status/', views.update_property_status, name='update_property_status'),
    path('acc_userview/', views.acc_userview, name="accomodation" ),
    path('acc_propertyview/', views.acc_propertyview, name="acc_propertyview" ),
    path('acc_listproperty/', views.acc_listproperty, name='acc_listproperty'),
    path('property/search/', views.property_search, name='property_search'),
    path('acc_booking/<int:property_id>/', views.acc_booking, name='acc_booking'),
    path('accpayment/<int:booking_id>/', views.accpayment, name='accpayment'),  # Add this line
    path('accpaymenthandler/<int:booking_id>/', views.accpaymenthandler, name='accpaymenthandler'),  # Add this line
    path('rentagreement/', views.rentagreement, name="rentagreement"),
    
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
