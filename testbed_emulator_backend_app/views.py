from django.shortcuts import render

from rest_framework import viewsets
from .models import AssemblyWorkflow
from .serializers import AssemblyWorkflowSerializer

class AssemblyWorkflowViewSet(viewsets.ModelViewSet):
    queryset = AssemblyWorkflow.objects.all()
    serializer_class = AssemblyWorkflowSerializer
