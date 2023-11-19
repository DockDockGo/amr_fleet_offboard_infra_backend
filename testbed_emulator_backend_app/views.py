from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from .models import AssemblyWorkflow, WorkCellState, AMRState, TestbedTask, MaterialTransportTaskChain, AMRMission
from .serializers import AssemblyWorkflowSerializer, WorkCellStateSerializer, AMRStateSerializer, TestbedTaskSerializer, MaterialTransportTaskChainSerializer, AMRMissionSerializer

class AssemblyWorkflowViewSet(viewsets.ModelViewSet):
    queryset = AssemblyWorkflow.objects.all()
    serializer_class = AssemblyWorkflowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model_assembly_type_id', 'fetch_parts_bins', 'kitting_task', 'assembly_task']
    # You can add more fields to filter by as needed

class WorkCellStateViewSet(viewsets.ModelViewSet):
    queryset = WorkCellState.objects.all()
    serializer_class = WorkCellStateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workcell_id', 'docked_amr_id']
    # Add other fields as needed

class AMRStateViewSet(viewsets.ModelViewSet):
    queryset = AMRState.objects.all()
    serializer_class = AMRStateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amr_id', 'active_mission']
    # Add other fields as needed

class TestbedTaskViewSet(viewsets.ModelViewSet):
    queryset = TestbedTask.objects.all()
    serializer_class = TestbedTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assembly_workflow_id', 'status', 'workcell_id']
    # Add other fields as needed

class MaterialTransportTaskChainViewSet(viewsets.ModelViewSet):
    queryset = MaterialTransportTaskChain.objects.all()
    serializer_class = MaterialTransportTaskChainSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assembly_workflow_id', 'navigate_to_source_subtask', 'loading_subtask']
    # Add other fields as needed

class AMRMissionViewSet(viewsets.ModelViewSet):
    queryset = AMRMission.objects.all()
    serializer_class = AMRMissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assembly_workflow_id', 'amr_id', 'start', 'goal', 'status', 'enqueue_time']
    # Add other fields as needed