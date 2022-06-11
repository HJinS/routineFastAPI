from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session


class EngineConn:

    __URL = 'postgresql://routine_fast:routine_fast@localhost/routine_fast_api'

    def __init__(self):
        self.engine = create_engine(self.__URL, echo=False)
        self.conn = None
        self.session = None

    def make_session(self, autocommit: bool = False, auto_flush: bool = True):
        _session = sessionmaker(autocommit=autocommit, autoflush=auto_flush, bind=self.engine)
        self.session = _session()
        return self.session

    def __enter__(self):
        self.make_session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
