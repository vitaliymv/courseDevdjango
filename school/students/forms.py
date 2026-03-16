from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "age", "score", "hours_studied"]

    def clean_score(self):
        score = self.cleaned_data.get("score")
        if score < 0 or score > 100:
            raise forms.ValidationError("Score must be between 0 and 100")
        return score

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 0 or age > 120:
            raise forms.ValidationError("Age must be between 0 and 120")
        return age

    def clean_hours_studied(self):
        hours = self.cleaned_data.get("hours_studied")
        if hours < 0 or hours > 24:
            raise forms.ValidationError("Hours studied must be between 0 and 24")
        return hours
