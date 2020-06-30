from sqlalchemy import create_engine, Table, Column, Integer, MetaData, engine, String
from sqlalchemy.orm import mapper, sessionmaker
from source.abstract.User import User
from os import environ


class Statistic:
    def __init__(self) -> None:
        self._engine: engine = create_engine(f'sqlite:///{environ.get("db_name", "supervisor.db")}', echo=False)
        self._session = sessionmaker(bind=self._engine)()
        self._table = None

    def create(self) -> None:
        metadata: MetaData = MetaData()
        self._table: Table = Table('stats', metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('imprisonment_counter', Integer, default=0),
                                   Column('total_time', Integer, default=0),
                                   Column('kicked_by', String, default="")
                                   )
        metadata.create_all(self._engine)
        mapper(User, self._table)

    @staticmethod
    def __decode_b64_array(content: bytes) -> list:
        from base64 import b64decode
        return b64decode(content).decode().split(';')

    def user_exists(self, id: int) -> bool:
        return bool([user for user in self._session.query(User).filter_by(id=id)])

    def add_user(self, id: int) -> None:
        if self.user_exists(id):
            return
        self._session.add(User(id=id))
        self._session.commit()

    def get_user(self, id: int) -> dict:
        for user in self._session.query(User).filter_by(id=id):
            user.kicked_by = Statistic.__decode_b64_array(str(user.kicked_by).encode())
            return dict(user)

    def get_sorted_users(self) -> list:
        data = self._session.query(User).order_by(self._table.c.total_time.desc()).all()
        for x in data:
            x.kicked_by = Statistic.__decode_b64_array(x.kicked_by)
        return data

    def increment_imprisonment_counter(self, id: int) -> None:
        for user in self._session.query(User).filter_by(id=id):
            user.imprisonment_counter += 1
        self._session.commit()

    def update_time(self, id: int, time: int) -> None:
        for user in self._session.query(User).filter_by(id=id):
            user.total_time += time
        self._session.commit()

    def add_dominus(self, prisoner_id: int, dominus_id: int) -> None:
        from base64 import b64encode
        for user in self._session.query(User).filter_by(id=prisoner_id):
            if user.kicked_by:
                _temp = Statistic.__decode_b64_array(user.kicked_by)
                _temp.append(str(dominus_id))
                user.kicked_by = b64encode(';'.join(_temp).encode())
            else:
                user.kicked_by = b64encode(str(dominus_id).encode())
        self._session.commit()
