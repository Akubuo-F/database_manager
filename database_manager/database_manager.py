from contextlib import contextmanager
from typing import Any, Generator, Optional
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


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
            raise ConnectionError(
                f"The error '{e}' was raised while trying to open a connection "
                "to the database."
                ) from e

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
            raise ConnectionError(
                f"The error '{e}' was raised while trying to get a session "
                "to the database."
            ) from e
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


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.open_connection(db_conn_url="YOUR-DATABASE-CONNECTION-URL", echo=False)
    with db_manager.get_session() as session:
        print("Database connection and session implemented correctly.")