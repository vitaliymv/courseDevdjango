from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    difficulty = models.IntegerField()

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    score = models.FloatField()
    hours_studied = models.FloatField()

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="students", null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name="students")

    def __str__(self):
        return self.name