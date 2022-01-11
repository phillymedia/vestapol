import logging
import pathlib
from vestapol.destinations import base_destination

logger = logging.getLogger(__name__)

class Local(base_destination.BaseDestination):
    def write_data(self, data: str, pathname: str):
        abs_pathname = self.create_local_folders(pathname)
        logger.debug(f"Writing data to {abs_pathname}")
        with abs_pathname.open(mode='w') as file:
            file.write(data)

    @staticmethod
    def create_local_folders(pathname):
        root_dir = pathlib.Path.cwd().resolve()
        extract_dir = root_dir / 'data'
        abs_pathname = extract_dir / pathname
        abs_pathname.parent.mkdir(parents=True, exist_ok=True)
        return abs_pathname

    def create_table(self, resource):
        return super().create_table(resource)
