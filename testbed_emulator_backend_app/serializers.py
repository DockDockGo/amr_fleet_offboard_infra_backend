from rest_framework import serializers
from .models import AssemblyWorkflow, TestbedTask, MaterialTransportTaskChain, AMRMission, WorkCellState, AMRState, TestbedTask, MaterialTransportTaskChain
from .testbed_config import WorkCell, TaskStatus, AMR, ASSEMBLY_WORKFLOW_PRESET

class AssemblyWorkflowSerializer(serializers.HyperlinkedModelSerializer):
    model_assembly_type_id = serializers.IntegerField()

    class Meta:
        model = AssemblyWorkflow
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assemblyworkflow-detail', 'lookup_field': 'pk'},
            'fetch_parts_bins': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'},
            'transport_parts_bins_to_kitting_station': {'view_name': 'materialtransporttaskchain-detail', 'lookup_field': 'pk'},
            'kitting_task': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'},
            'transport_kitting_task_payload_to_assembly_station': {'view_name': 'materialtransporttaskchain-detail', 'lookup_field': 'pk'},
            'assembly_task': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'},
            'transport_assembly_task_payload_to_qa_station': {'view_name': 'materialtransporttaskchain-detail', 'lookup_field': 'pk'}
            # Add other FK fields as URLs if needed
        }

    def create(self, validated_data):
        preset = ASSEMBLY_WORKFLOW_PRESET
        model_assembly_type_id = validated_data.get('model_assembly_type_id')

        # Create AssemblyWorkflow instance first without linking tasks and chains
        assembly_workflow = AssemblyWorkflow.objects.create(model_assembly_type_id=model_assembly_type_id)

        # Now create TestbedTask and MaterialTransportTaskChain instances
        # Make sure to link them with the newly created AssemblyWorkflow
        fetch_parts_bins = TestbedTask.objects.create(
            assembly_workflow_id=assembly_workflow.id, **preset['fetch_parts_bins'])
        kitting_task = TestbedTask.objects.create(
            assembly_workflow_id=assembly_workflow.id, **preset['kitting_task'])
        assembly_task = TestbedTask.objects.create(
            assembly_workflow_id=assembly_workflow.id, **preset['assembly_task'])

        # Updating AssemblyWorkflow with created tasks
        assembly_workflow.fetch_parts_bins = fetch_parts_bins
        assembly_workflow.kitting_task = kitting_task
        assembly_workflow.assembly_task = assembly_task

        # Create MaterialTransportTaskChains similarly and link them to AssemblyWorkflow
        transport_parts_bins_to_kitting_station = self.create_material_transport_chain(
            assembly_workflow.id, preset['transport_parts_bins_to_kitting_station'])
        transport_kitting_task_payload_to_assembly_station = self.create_material_transport_chain(
            assembly_workflow.id, preset['transport_kitting_task_payload_to_assembly_station'])
        transport_assembly_task_payload_to_qa_station = self.create_material_transport_chain(
            assembly_workflow.id, preset['transport_assembly_task_payload_to_qa_station'])

        # Linking TransportTaskChains to AssemblyWorkflow
        assembly_workflow.transport_parts_bins_to_kitting_station = transport_parts_bins_to_kitting_station
        assembly_workflow.transport_kitting_task_payload_to_assembly_station = transport_kitting_task_payload_to_assembly_station
        assembly_workflow.transport_assembly_task_payload_to_qa_station = transport_assembly_task_payload_to_qa_station

        # Save the updated AssemblyWorkflow
        assembly_workflow.save()

        return assembly_workflow

    def create_material_transport_chain(self, assembly_workflow_id, chain_data):
        navigate_to_source_subtask = AMRMission.objects.create(
            assembly_workflow_id=assembly_workflow_id, **chain_data['navigate_to_source_subtask'])
        loading_subtask = TestbedTask.objects.create(
            assembly_workflow_id=assembly_workflow_id, **chain_data['loading_subtask'])
        navigate_to_sink_subtask = AMRMission.objects.create(
            assembly_workflow_id=assembly_workflow_id, **chain_data['navigate_to_sink_subtask'])
        unloading_subtask = TestbedTask.objects.create(
            assembly_workflow_id=assembly_workflow_id, **chain_data['unloading_subtask'])

        material_transport_task_chain = MaterialTransportTaskChain.objects.create(
            assembly_workflow_id=assembly_workflow_id,
            navigate_to_source_subtask=navigate_to_source_subtask,
            loading_subtask=loading_subtask,
            navigate_to_sink_subtask=navigate_to_sink_subtask,
            unloading_subtask=unloading_subtask
        )

        # Set the material_transport_task_chain_id for each task
        navigate_to_source_subtask.material_transport_task_chain_id = material_transport_task_chain.id
        loading_subtask.material_transport_task_chain_id = material_transport_task_chain.id
        navigate_to_sink_subtask.material_transport_task_chain_id = material_transport_task_chain.id
        unloading_subtask.material_transport_task_chain_id = material_transport_task_chain.id

        # Don't forget to save these objects after updating them
        navigate_to_source_subtask.save()
        loading_subtask.save()
        navigate_to_sink_subtask.save()
        unloading_subtask.save()
        
        return material_transport_task_chain


class WorkCellStateSerializer(serializers.HyperlinkedModelSerializer):
    workcell_id = serializers.CharField()
    docked_amr_id = serializers.CharField()

    class Meta:
        model = WorkCellState
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'workcellstate-detail', 'lookup_field': 'pk'},
            'active_task': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'}
            # Add other FK fields here if needed
        }


class AMRStateSerializer(serializers.HyperlinkedModelSerializer):
    amr_id = serializers.CharField()

    class Meta:
        model = AMRState
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'amrstate-detail', 'lookup_field': 'pk'},
            'active_mission': {'view_name': 'amrmission-detail', 'lookup_field': 'pk'}
        }

class TestbedTaskSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField()
    assembly_workflow_id = serializers.IntegerField(allow_null=True, required=False)
    workcell_id = serializers.CharField()
    material_transport_task_chain_id = serializers.IntegerField(allow_null=True, required=False)


    class Meta:
        model = TestbedTask
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'}
            # Add other FK fields here if needed
        }

class AMRMissionSerializer(serializers.HyperlinkedModelSerializer):
    amr_id = serializers.IntegerField(allow_null=True, required=False)
    assembly_workflow_id = serializers.IntegerField(allow_null=True, required=False)
    start = serializers.IntegerField()
    goal = serializers.IntegerField()
    status = serializers.IntegerField()
    material_transport_task_chain_id = serializers.IntegerField(allow_null=True, required=False)
    
    class Meta:
        model = AMRMission
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'amrmission-detail', 'lookup_field': 'pk'},
            # Add other FK fields as URLs if needed
            # For example:
            # 'amr_id': {'view_name': 'amrstate-detail', 'lookup_field': 'pk'}
        }

class MaterialTransportTaskChainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialTransportTaskChain
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'materialtransporttaskchain-detail', 'lookup_field': 'pk'},
            'navigate_to_source_subtask': {'view_name': 'amrmission-detail', 'lookup_field': 'pk'},
            'loading_subtask': {'view_name': 'testbedtask-detail', 'lookup_field': 'pk'},
            # Continue for other FK fields
        }