from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class AsyncDB:
    def __init__(self, db_type: str, db_name: str) -> None:
        """AsyncDB

        Args:
            db_type (str): Type of your db, for example: sqlite, sqlite3
            db_name (str): Name of your db
        """
        # self.engine = create_engine(f"{db_type}:///{db_name}.db")
        self.__engine = None
        self.session = None
        self.__set_engine(db_type, db_name)

    def __set_engine(self, db_type, db_name):
        try:
            self.__engine = create_engine(f"{db_type}:///{db_name}.db")
        except Exception as e:
            # print(e)
            self.__engine = create_engine(f"sqlite:///base.db")
        finally:
            self.session = sessionmaker(bind=self.__engine)

    def up(self):
        Base.metadata.create_all(self.__engine)

    def down(self):
        Base.metadata.drop_all(self.__engine)

    def migrate(self):
        Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

    def get_session(self):
        with self.session.begin() as session:
            yield session


from .models import Task


tasks_db = AsyncDB("sqlite", "tasks")
# mydb = AsyncDB("sqlite", "tasks")
# faildb = AsyncDB("jopa", "tasks")
# print(mydb.__dict__)
# print(faildb.__dict__)
