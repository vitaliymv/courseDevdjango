from django.urls import path
from .views import StudentListView, StudentCreateView, LoadTestDataView, TeacherListView, CourseListView

urlpatterns = [
    path("", StudentListView.as_view(), name="student_list"),
    path("add/", StudentCreateView.as_view(), name="student_add"),
    path("load-test-data/", LoadTestDataView.as_view(), name="load_test_data"),
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("courses/", CourseListView.as_view(), name="course_list"),
]