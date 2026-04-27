from django.urls import path
from .views import ReportListView, ReportCreateView

urlpatterns = [
    path('', ReportListView.as_view(), name='report_list'),
    path('create/', ReportCreateView.as_view(), name='create_report'),
]