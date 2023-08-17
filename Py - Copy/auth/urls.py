from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', views.log_in, name='log_in'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Corrected view
    path('', views.home, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
]
