from django.db import models
from .testbed_config import AMR, TaskStatus, WorkCell
from django.db.models import Q

# # A work cell is a physical location in the factory where a robot can be assigned to perform a task
# class WorkCell(Enum):
#     STOCK_ROOM = 1
#     KITTING_STATION = 2
#     ASSEMBLY_STATION_1 = 3
#     ASSEMBLY_STATION_2 = 4
#     QA_STATION = 5


# class TaskStatus(Enum):
#     BACKLOG = 1
#     ENQUEUED = 2
#     RUNNING = 3
#     COMPLETED = 4
#     FAILED = 5
#     CANCELED = 6


# # An AMR is an autonomous mobile robot. We currently have the following 2 robots at the testbed
# class AMR(Enum):
#     RICK = 1
#     MORTY = 2


# # Dictionary mapping workcell to int type dock ids
# # For now, we use the same fiducial marker id as the dock id
# WORKCELL_TO_DOCK_IDS = {
#     WorkCell.STOCK_ROOM: 1,
#     WorkCell.KITTING_STATION: 2,
#     WorkCell.ASSEMBLY_STATION_1: 3,
#     WorkCell.ASSEMBLY_STATION_2: 4,
#     WorkCell.QA_STATION: 5,
# }


class WorkCellState(models.Model):
    workcell_id = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in WorkCell]
    )
    active_task = models.OneToOneField(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True
    )
    # add a field for the AMR id that is currently docked at this workcell
    docked_amr_id = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in AMR], null=True, blank=True
    )

    def __str__(self):
        active_task_str = f"{self.active_task}" if self.active_task else "None"
        return f"WorkCellState: {self.workcell_id} <active_task: {active_task_str}, docked_amr_id: {self.docked_amr_id}>"


class AMRState(models.Model):
    amr_id = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in AMR])
    active_mission = models.OneToOneField(
        "AMRMission", on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        active_mission_str = f"{self.active_mission}" if self.active_mission else "None"
        return f"AMRState for amr_id: {self.amr_id} <active_mission: {active_mission_str}>"



class Task(models.Model):
    assembly_workflow_id = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in TaskStatus], default=TaskStatus.BACKLOG.value
    )
    # Creation and update time fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Time at which the task is 'enqueued', should default to None
    enqueue_time = models.DateTimeField(null=True, blank=True)
    # Task chronography for performance metrics
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def query_assembly_workflow_id(self):
        # Check for direct relation to AssemblyWorkflow
        direct_related_workflow = AssemblyWorkflow.objects.filter(
            Q(fetch_parts_bins=self) |
            Q(kitting_task=self) |
            Q(assembly_task=self)
        ).first()

        if direct_related_workflow:
            return direct_related_workflow.id

        # Check relation through MaterialTransportTaskChain
        # This part assumes that Task is related to MaterialTransportTaskChain via a OneToOneField or ForeignKey
        related_task_chains = MaterialTransportTaskChain.objects.filter(
            Q(navigate_to_source_subtask=self) |
            Q(loading_subtask=self) |
            Q(navigate_to_sink_subtask=self) |
            Q(unloading_subtask=self)
        )

        for task_chain in related_task_chains:
            # Traverse to AssemblyWorkflow
            if task_chain.transport_parts_bins_to_kitting_station_assembly_workflow:
                return task_chain.transport_parts_bins_to_kitting_station_assembly_workflow.id
            if task_chain.transport_kitting_task_payload_to_assembly_station_assembly_workflow:
                return task_chain.transport_kitting_task_payload_to_assembly_station_assembly_workflow.id
            if task_chain.transport_assembly_task_payload_to_qa_station_assembly_workflow:
                return task_chain.transport_assembly_task_payload_to_qa_station_assembly_workflow.id

        return None  # Or appropriate default value

    # Abstract base class
    class Meta:
        abstract = True


class TestbedTask(Task):
    workcell_id = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in WorkCell]
    )

    def __str__(self):
        return f"TestbedTask: {self.assembly_workflow_id} <status: {self.status}, workcell_id: {self.workcell_id}>"


class AMRMission(Task):
    amr_id = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in AMR])
    start = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in WorkCell]
    )
    goal = models.CharField(
        max_length=20, choices=[(tag, tag.value) for tag in WorkCell]
    )

    def __str__(self):
        return f"AMRMission: {self.assembly_workflow_id} <status: {self.status}, amr_id: {self.amr_id}, start: {self.start}, goal: {self.goal}>"

# MaterialTransportTaskChain represents a chain of tasks:
# 1. An AMR mission called NavigateToSourceSubTask that represents the AMR navigating to the source workcell
# 2. A TestbedTask called LoadingSubTask that represents the operator / testbed robot arm placing the payload on the AMR
# 3. An AMR mission called NavigateToSinkSubTask that represents the AMR navigating to the destination workcell
# 4. A TestbedTask called UnloadingSubTask that represents the operator / testbed robot arm removing the payload from the AMR
# Use onetoone relationshipsto link to the subtasks within this new model
# add a model property that checks the status of all the subtasks and returns a dictionary of the statuses
class MaterialTransportTaskChain(models.Model):
    assembly_workflow_id = models.IntegerField()
    navigate_to_source_subtask = models.OneToOneField(
        "AMRMission", on_delete=models.PROTECT, null=True, blank=True,
        related_name="navigate_to_source_subtask_material_transport_task_chain",
    )
    loading_subtask = models.OneToOneField(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True,
        related_name="loading_subtask_material_transport_task_chain",
    )
    navigate_to_sink_subtask = models.OneToOneField(
        "AMRMission", on_delete=models.PROTECT, null=True, blank=True,
    )
    unloading_subtask = models.OneToOneField(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True,
        related_name="unloading_subtask_material_transport_task_chain",
    )

    @property
    def subtask_status(self):
        return {
            "navigate_to_source_subtask": self.navigate_to_source_subtask.status,
            "loading_subtask": self.loading_subtask.status,
            "navigate_to_sink_subtask": self.navigate_to_sink_subtask.status,
            "unloading_subtask": self.unloading_subtask.status,
        }

    def description(self):
        navigate_to_source_subtask_str = f"{self.navigate_to_source_subtask}" if self.navigate_to_source_subtask else "None"
        loading_subtask_str = f"{self.loading_subtask}" if self.loading_subtask else "None"
        navigate_to_sink_subtask_str = f"{self.navigate_to_sink_subtask}" if self.navigate_to_sink_subtask else "None"
        unloading_subtask_str = f"{self.unloading_subtask}" if self.unloading_subtask else "None"

        return f"MaterialTransportTaskChain: {self.assembly_workflow_id} <status: {self.status}, navigate_to_source_subtask: {navigate_to_source_subtask_str}, loading_subtask: {loading_subtask_str}, navigate_to_sink_subtask: {navigate_to_sink_subtask_str}, unloading_subtask: {unloading_subtask_str}>"

    def query_assembly_workflow_id(self):
        if self.transport_parts_bins_to_kitting_station_assembly_workflow:
            return self.transport_parts_bins_to_kitting_station_assembly_workflow.id
        if self.transport_kitting_task_payload_to_assembly_station_assembly_workflow:
            return self.transport_kitting_task_payload_to_assembly_station_assembly_workflow.id
        if self.transport_assembly_task_payload_to_qa_station_assembly_workflow:
            return self.transport_assembly_task_payload_to_qa_station_assembly_workflow.id
        return None  # Or appropriate default value

# Now let's create a new model called AssemblyWorkflow that represents a workflow that the testbed is executing. An assembly workflow consists of the following TestbedTasks and MaterialTransportTaskChains:
# 1. A TestbedTask called FetchPartsBins that represents the operator / testbed robot arm fetching the parts bins from the stock room.
# 2. A MaterialTransportTaskChain called TransportPartsBinsToKittingStation that represents the operator / testbed robot arm placing the parts bins on the AMR and the AMR transporting the parts bins to the kitting station.
# 3. A TestbedTask called kitting_task that represents the operator / testbed robot arm performing the kitting task.
# 4. A MaterialTransportTaskChain called TransportKittingTaskPayloadToAssemblyStation that represents the operator / testbed robot arm placing the payload on the AMR and the AMR transporting the payload to the assembly station.
# 5. A TestbedTask called assembly_task that represents the operator / testbed robot arm performing the assembly task.
# 6. A MaterialTransportTaskChain called TransportAssemblyTaskPayloadToQaStation that represents the operator / testbed robot arm placing the payload on the AMR and the AMR transporting the payload to the QA station.
class AssemblyWorkflow(models.Model):
    model_assembly_type_id = models.IntegerField()
    fetch_parts_bins = models.ForeignKey(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True,
        related_name="fetch_parts_bins_assembly_workflow",
    )
    transport_parts_bins_to_kitting_station = models.ForeignKey(
        "MaterialTransportTaskChain", on_delete=models.PROTECT, null=True, blank=True,
        related_name="transport_parts_bins_to_kitting_station_assembly_workflow",
    )
    kitting_task = models.ForeignKey(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True,
        related_name="kitting_task_assembly_workflow",
    )
    transport_kitting_task_payload_to_assembly_station = models.ForeignKey(
        "MaterialTransportTaskChain", on_delete=models.PROTECT, null=True, blank=True,
        related_name="transport_kitting_task_payload_to_assembly_station_assembly_workflow",
    )
    assembly_task = models.ForeignKey(
        "TestbedTask", on_delete=models.PROTECT, null=True, blank=True,
        related_name="assembly_task_assembly_workflow",
    )
    transport_assembly_task_payload_to_qa_station = models.ForeignKey(
        "MaterialTransportTaskChain", on_delete=models.PROTECT, null=True, blank=True,
        related_name="transport_assembly_task_payload_to_qa_station_assembly_workflow",
    )

    @property
    def status_dict(self):
        return {
            "fetch_parts_bins": self.fetch_parts_bins.status,
            "transport_parts_bins_to_kitting_station": self.transport_parts_bins_to_kitting_station.subtask_status,
            "kitting_task": self.kitting_task.status,
            "transport_kitting_task_payload_to_assembly_station": self.transport_kitting_task_payload_to_assembly_station.subtask_status,
            "assembly_task": self.assembly_task.status,
            "transport_assembly_task_payload_to_qa_station": self.transport_assembly_task_payload_to_qa_station.subtask_status,
        }


    def description(self):
        fetch_parts_bins_str = f"{self.fetch_parts_bins}" if self.fetch_parts_bins else "None"
        transport_parts_bins_to_kitting_station_str = f"{self.transport_parts_bins_to_kitting_station}" if self.transport_parts_bins_to_kitting_station else "None"
        kitting_task_str = f"{self.kitting_task}" if self.kitting_task else "None"
        transport_kitting_task_payload_to_assembly_station_str = f"{self.transport_kitting_task_payload_to_assembly_station}" if self.transport_kitting_task_payload_to_assembly_station else "None"
        assembly_task_str = f"{self.assembly_task}" if self.assembly_task else "None"
        transport_assembly_task_payload_to_qa_station_str = f"{self.transport_assembly_task_payload_to_qa_station}" if self.transport_assembly_task_payload_to_qa_station else "None"

        return f"AssemblyWorkflow: {self.id} <status: {self.status}, fetch_parts_bins: {fetch_parts_bins_str}, transport_parts_bins_to_kitting_station: {transport_parts_bins_to_kitting_station_str}, kitting_task: {kitting_task_str}, transport_kitting_task_payload_to_assembly_station: {transport_kitting_task_payload_to_assembly_station_str}, assembly_task: {assembly_task_str}, transport_assembly_task_payload_to_qa_station: {transport_assembly_task_payload_to_qa_station_str}>"