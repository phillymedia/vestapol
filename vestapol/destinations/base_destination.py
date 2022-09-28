from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vestapol.web_resources.base_resource import BaseResource


class BaseDestination(ABC):
    @abstractmethod
    def write_data(self, data: str, pathname: str):
        pass

    @abstractmethod
    def create_table(self, resource: BaseResource):
        """
        Implementations of method should return the fully-qualified table name
        of the created table
        :rtype: str
        """
        raise NotImplementedError
