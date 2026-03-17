from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
from .models import Student, Teacher, Course
from django.urls import reverse_lazy
from .forms import StudentForm
from faker import Faker
import random
from django.db.models import Avg, Count, F, Q
import json

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "add.html"
    success_url = reverse_lazy("student_list")

fake = Faker()

class LoadTestDataView(View):
    def get(self, request, *args, **kwargs):
        teachers = []
        for _ in range(3):
            teacher = Teacher.objects.create(
                name=fake.name(),
                experience_years=random.randint(1, 20)
            )
            teachers.append(teacher)

        courses_data = [
            {"title": "Python", "difficulty": 3},
            {"title": "Django", "difficulty": 4},
            {"title": "Data Science", "difficulty": 5},
            {"title": "Machine Learning", "difficulty": 5},
        ]
        courses = [Course.objects.create(**c) for c in courses_data]

        students = []
        for _ in range(12):
            student = Student.objects.create(
                name=fake.first_name(),
                age=random.randint(18, 25),
                score=random.randint(70, 100),
                hours_studied=random.randint(1, 24),
                teacher=random.choice(teachers),
            )
            student_courses = random.sample(courses, k=random.randint(1, 3))
            student.courses.set(student_courses)
            students.append(student)
        return HttpResponse(f"Created {len(teachers)} teachers, {len(courses)} courses, {len(students)} students with Faker data!")

class StudentListView(ListView):
    model = Student
    template_name = "list.html"
    context_object_name = "students"

    def get_queryset(self):
        return Student.objects.select_related(
            "teacher"
        ).prefetch_related(
            "courses"
        ).filter(
            score__gt=80
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top3"] = Student.objects.order_by("-score")[:3]
        context["q_filtered"] = Student.objects.filter(
            Q(score__gt=90) | Q(hours_studied__gt=5)
        )
        return context

class TeacherListView(ListView):
    model = Teacher
    template_name = "teachers.html"
    context_object_name = "teachers"

    def get_queryset(self):
        return Teacher.objects.annotate(
            avg_score=Avg("students__score")
        )

class CourseListView(ListView):
    model = Course
    template_name = "courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.annotate(
            student_count=Count("students")
        ).filter(
            student_count__gt=2
        )

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Student.objects.aggregate(
            total_students=Count("id"),
            avg_score=Avg("score"),
        )
        # number of students, average,
        # number of courses, number of teachers
        context["total_students"] = stats["total_students"]
        context["avg_score"] = round(stats["avg_score"] or 0, 2)
        context["total_courses"] = Course.objects.count()
        context["total_teachers"] = Teacher.objects.count()

        # number of students in each course
        courses = Course.objects.annotate(
            student_count=Count("students")
        )
        course_labels = [c.title for c in courses]
        course_data = [c.student_count for c in courses]

        context["course_labels"] = json.dumps(course_labels)
        context["course_data"] = json.dumps(course_data)
        # courses by difficulty
        difficulty_data = Course.objects.values(
            "difficulty"
        ).annotate(
            count=Count("id")
        )
        context["diff_labels"] = json.dumps(
            [
                str(d["difficulty"])
                for d in difficulty_data
            ]
        )
        context["diff_data"] = json.dumps(
            [
                d["count"]
                for d in difficulty_data
            ]
        )

        # average score of students for each teacher
        teachers = Teacher.objects.annotate(
            avg_score=Avg("students__score")
        )
        teacher_labels = [
            t.name
            for t in teachers
        ]
        teacher_data = [
            round(t.avg_score or 0, 2)
            for t in teachers
        ]
        context["teacher_labels"] = json.dumps(teacher_labels)
        context["teacher_data"] = json.dumps(teacher_data)

        # age distribution
        age_data = Student.objects.values(
            "age"
        ).annotate(
            count=Count("id")
        ).order_by("age")
        age_labels = [
            str(a["age"])
            for a in age_data
        ]
        age_counts = [
            a["count"]
            for a in age_data
        ]
        context["age_labels"] = json.dumps(age_labels)
        context["age_data"] = json.dumps(age_counts)

        return context