from vestapol.destinations.base_destination import BaseDestination


def write_text(data: str, pathname: str, destination: BaseDestination):
    destination.write_data(data, pathname)
