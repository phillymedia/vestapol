from __future__ import annotations
import logging
import pathlib
from vestapol.destinations import base_destination
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vestapol.typing.resources import ResourceTypes

logger = logging.getLogger(__name__)


class Local(base_destination.BaseDestination):
    def write_data(self, data: str, pathname: str):
        abs_pathname = self.create_local_folders(pathname)
        logger.debug(f"Writing data to {abs_pathname}")
        with abs_pathname.open(mode="w") as file:
            file.write(data)

    @staticmethod
    def create_local_folders(pathname: str):
        root_dir = pathlib.Path.cwd().resolve()
        extract_dir = root_dir / "data"
        abs_pathname = extract_dir / pathname
        abs_pathname.parent.mkdir(parents=True, exist_ok=True)
        return abs_pathname

    def create_table(self, resource: ResourceTypes):
        return super().create_table(resource)
