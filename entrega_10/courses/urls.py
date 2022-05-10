from django.urls import path

from courses.views import (
    CourseByIdView,
    CourseView,
    registerInstructorInCourse,
    registerStudentsInCourse,
)

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<str:course_id>/', CourseByIdView.as_view()),
    path('courses/<course_id>/registrations/instructor/', registerInstructorInCourse),
    path('courses/<course_id>/registrations/students/', registerStudentsInCourse),
]