from contextlib import contextmanager
from typing import Optional
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from database_manager.entities.entity import Entity


class DatabaseManager:
    """
    Manages sqlalchemy connections and sessions.
    """

    def __init__(self) -> None:
        """
        Initialise the database manager.
        """
        self._engine: Optional[Engine] = None

    
    def open_connection(self, db_conn_url: str, echo: bool = False) -> None:
        """
        Opens a connection to the database.

        Params:
            db_conn_url (str): The database connection url.
            echo (bool): Indicates whether events in the database should be logged out
                to the console. Defaults to True.

        Raises:
            ConnectionError: If there is an existing connection to the database.
        """
        if self._engine:
            raise ConnectionError("Connection to the database already exists.")
        
        try:
            self._engine = create_engine(db_conn_url, echo=echo)
        except Exception as e:
            raise ConnectionError() from e

    @contextmanager
    def get_session(self):
        """
        Yields a session to the database. Auto commits all transaction when done with session.

        Raises:
            ConnectionError: If there isn't an existing connection to the database
        """
        if not self._engine:
            raise ConnectionError("There is no existing connection to the database.")
        
        session = Session(bind=self._engine, autocommit=False, autoflush=False)

        try:
            yield session
        except Exception as e:
            session.rollback()
            raise ConnectionError() from e
        finally:
            session.commit()
            session.close()

    
    def close_connection(self) -> None:
        """
        Closes the existing connection if any.
        """
        if self._engine:
            self._engine.dispose()
            self._engine = None


    def init_tables(self) -> None:
        """
        Creates all tables. Make sure all database entities are imported first
        before calling this method.
        """
        if self._engine:
            Entity.metadata.create_all(bind=self._engine)
