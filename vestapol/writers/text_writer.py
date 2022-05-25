from vestapol.destinations import DestinationTypes


def write_text(data: str, pathname: str, destination: DestinationTypes):
    destination.write_data(data, pathname)
