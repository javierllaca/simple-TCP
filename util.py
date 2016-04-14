import os
import struct
import sys
import time


def checksum(data):
    s = 0
    if len(data) % 2 == 1:
        data += '\x00'  # make number of bytes even
    for i in range(0, len(data), 2):
        s += ord(data[i]) + (ord(data[i + 1]) << 8)
        s = (s & 0xffff) + (s >> 16)
    return ~s & 0xffff


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


def current_time():
    return time.time()


def current_time_string():
    return time.strftime('%m-%d-%yT%H:%M:%S')
