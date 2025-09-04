from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

from database_manager.entities.entity import Entity


T = TypeVar("T", bound="EntityModel", covariant=True)
E = TypeVar("E", bound=Entity)


class EntityModel(Protocol, Generic[T, E]):
    """
    Contract for data models that can be converted to/from domain
    entities.

    This protocol ensures that data layer models can:
    1. Convert themeselves to domain entities (to_entity)
    2. Create instances from domain entities (from_entity)

    Type Parameters:
        T: The concrete model type implementing this protocol
        E: The specific entity type this model converts to/from

    Example:
        ```python
        class UserModel(EntityModel[UserModel, UserEntity]):
                def to_entity(self) -> UserEntity: 
                    ...

                @classmethod
                def from_entity(cls, entity: User) -> UserModel: 
                    ...
        ```
    """

    @abstractmethod
    def to_entity(self) -> E:
        """
        Converts this model instance to a domain entity.

        Returns:
            E: The corresponding domain entity of type E
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: E) -> T:
        """
        Creates a model instance from a domain entity.

        Params:
            entity: The domain entity to convert from
        
        Returns:
            T: New instance of the model type
        """
        raise NotImplementedError