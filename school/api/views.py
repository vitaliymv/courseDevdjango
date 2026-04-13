from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTaskSerializer

class CustomTaskAPIView(APIView):
    def post(self, request):
        serializer = CustomTaskSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        is_completed = self.request.query_params.get("is_completed")

        if is_completed is not None:
            if is_completed.lower() == "true":
                queryset = queryset.filter(is_completed=True)
            elif is_completed.lower() == "false":
                queryset = queryset.filter(is_completed=False)

        return queryset

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.save()

        return Response({"status": "Task completed"})