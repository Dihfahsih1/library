from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from .views import *
app_name = "Profile"

urlpatterns = [
  path('student/signup/', student_signup.as_view(), name="student-signup")
]
