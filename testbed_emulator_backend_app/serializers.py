from rest_framework import serializers
from .models import AssemblyWorkflow, TestbedTask, MaterialTransportTaskChain, AMRMission
from .testbed_config import WorkCell, TaskStatus, AMR, ASSEMBLY_WORKFLOW_PRESET

class AssemblyWorkflowSerializer(serializers.ModelSerializer):
    model_assembly_type_id = serializers.IntegerField()

    class Meta:
        model = AssemblyWorkflow
        fields = ['id', 'model_assembly_type_id']

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
        
        return material_transport_task_chain
