from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import assign_tasks

class AssignTasksReportView(APIView):
    def get(self, request):
        assignments = assign_tasks()
        return Response(assignments, status=status.HTTP_200_OK)
