import logging


def write_text(data: str, pathname, destination):
    destination.write_data(data, pathname)
