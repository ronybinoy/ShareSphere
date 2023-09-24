# custom_filters.py

from django import template
from main.models import Course_Application  # Replace 'your_app' with your app's name

register = template.Library()

@register.filter
def course_already_applied(course, user):
    return Course_Application.objects.filter(course=course, user=user).exists()
