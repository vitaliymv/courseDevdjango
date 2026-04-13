from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CustomTaskAPIView

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("custom-task/", CustomTaskAPIView.as_view()),
    path("", include(router.urls)),
]