from sqlalchemy.orm import Mapped

from .. import Base


class Task(Base):
    __tablename__ = "Tasks"
    name: Mapped[str]
    author: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[str]
