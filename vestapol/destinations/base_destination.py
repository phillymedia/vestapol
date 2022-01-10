from abc import ABC, abstractmethod


class BaseDestination(ABC):

    @abstractmethod
    def write_data(self, data: str, pathname: str):
        pass

    @abstractmethod
    def create_table(self, resource):
        """
        Implementations of method should return the fully-qualified table name
        of the created table 
        :rtype: str
        """
        raise NotImplementedError
