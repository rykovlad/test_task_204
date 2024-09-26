import enum

class TaskStatus(enum.Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


class TaskPriority(enum.Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class UserRole(enum.Enum):
    PO = "Product Owner"
    TEAMLEAD = "Team Lead"
    DEV = "Developer"
    DESIGNER = "Designer"
    QA = "Quality Assurance"
