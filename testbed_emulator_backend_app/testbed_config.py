from enum import Enum

FLEET_INFRA_IP_AND_PORT = "0.0.0.0:5001"


# A work cell is a physical location in the factory where a robot can be assigned to perform a task
class WorkCell(Enum):
    STOCK_ROOM = 1
    KITTING_STATION = 2
    ASSEMBLY_STATION_1 = 3
    ASSEMBLY_STATION_2 = 4
    QA_STATION = 5


class TaskStatus(Enum):
    BACKLOG = 1
    ENQUEUED = 2
    RUNNING = 3
    COMPLETED = 4
    FAILED = 5
    CANCELED = 6


# An AMR is an autonomous mobile robot. We currently have the following 2 robots at the testbed
class AMR(Enum):
    RICK = 1
    MORTY = 2


# Dictionary mapping workcell to int type dock ids
# For now, we use the same fiducial marker id as the dock id
WORKCELL_TO_DOCK_IDS = {
    WorkCell.STOCK_ROOM: 1,
    WorkCell.KITTING_STATION: 2,
    WorkCell.ASSEMBLY_STATION_1: 3,
    WorkCell.ASSEMBLY_STATION_2: 4,
    WorkCell.QA_STATION: 5,
}
