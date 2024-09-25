from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import enum

from create_db import engine

Base = declarative_base()


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


task_responsible = Table(
    'task_responsible',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

task_executors = Table(
    'task_executors',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    passwd = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    tasks_responsible = relationship('Task',
                         secondary=task_responsible,
                         back_populates='responsible')
    tasks_executor = relationship('Task',
                         secondary=task_executors,
                         back_populates='executors')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)

    responsible = relationship('User', secondary=task_responsible, back_populates='tasks_responsible')
    executors = relationship('User', secondary=task_executors, back_populates='tasks_executor')


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # Creating a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # An example of adding data to tables

    new_user1 = User(
        name="Alice",
        email="alice@example.com",
        passwd="alicepassword",
        role=UserRole.PO
    )
    new_user2 = User(
        name="Bob",
        email="bob@example.com",
        passwd="bobpassword",
        role=UserRole.DEV
    )
    new_task = Task(
        name="first task",
        description="desc of first task",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        # executors=[new_user2.id],
        # responsible=new_user1.id
    )

    # Saving changes in the database
    session.add(new_user1)
    session.add(new_user2)
    session.add(new_task)

    new_task.responsible.append(new_user1)
    new_task.executors.append(new_user2)

    session.commit()

    session.close()