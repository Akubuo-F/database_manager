"""
Database Manager - A Python package for database management with PostgreSQL support.

This package provides a clean, object-oriented interface for managing database
connections and sessions using SQLAlchemy with PostgreSQL support.

Modules:
    DatabaseManager: Main class for managing database connections and sessions
    Entity: Base class for all database entities using SQLAlchemy's DeclarativeBase
    EntityModel: Protocol for data models that convert to/from domain entities

Example:
    >>> from database_manager import DatabaseManager, Entity, EntityModel
    >>> 
    >>> # Create a database manager
    >>> db_manager = DatabaseManager()
    >>> db_manager.open_connection("postgresql://user:pass@localhost/db")
    >>> 
    >>> # Define an entity
    >>> class User(Entity):
    ...     __tablename__ = "users"
    ...     # Add your columns here
    >>> 
    >>> # Use the session
    >>> with db_manager.get_session() as session:
    ...     # Perform database operations
    ...     pass
"""

from .database_manager import DatabaseManager
from .entities.entity import Entity
from .contracts.entity_model import EntityModel

__all__ = [
    "DatabaseManager",
    "Entity", 
    "EntityModel",
]

__version__ = "0.1.0"
__author__ = "Favour Chigoziri Akubuo"
__email__ = "akubuof.work@gmail.com"
__description__ = "A Python database manager with PostgreSQL support"
