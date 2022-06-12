from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class EngineConn:

    __URL = 'postgresql://routine_fast:routine_fast@localhost/routine_fast_api'

    def __init__(self):
        self.engine = create_engine(self.__URL, echo=False)
        self.__conn = None
        self.__session = None

    def make_session(self, auto_commit: bool = False, auto_flush: bool = True):
        _session = sessionmaker(autocommit=auto_commit, autoflush=auto_flush, bind=self.engine)
        self.__session = _session()
        return self.__session

    def __enter__(self):
        self.__conn = self.engine.connect()
        return self.__conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__conn.close()


@contextmanager
def session_scope():
    db_engine = EngineConn()
    session = db_engine.make_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
