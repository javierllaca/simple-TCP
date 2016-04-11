import os
import sys


# TODO: implement segment checksum
def checksum(data):
    return 0


def open_read_file(path):
    if os.path.isfile(path):
        return open(path, 'rb')
    else:
        raise IOError('\'{}\' does not exist'.format(path))


def open_write_file(path):
    if path == 'stdout':
        return sys.stdout
    if not os.path.isfile(path):
        return open(path, 'wb')
    else:
        raise IOError('\'{}\' already exist'.format(path))
