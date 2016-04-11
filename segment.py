from collections import OrderedDict
from ctypes import addressof, c_byte, c_uint, memmove, sizeof, Structure
import time
import util

MSS = 576


class TCPSegment(Structure):

    _fields_ = [
        ('src_port', c_uint, 16),
        ('dst_port', c_uint, 16),
        ('seq_num', c_uint, 32),
        ('ack_num', c_uint, 32),
        ('hdr_len', c_uint, 4),
        ('unused', c_uint, 6),
        ('URG', c_uint, 1),
        ('ACK', c_uint, 1),
        ('PSH', c_uint, 1),
        ('RST', c_uint, 1),
        ('SYN', c_uint, 1),
        ('FIN', c_uint, 1),
        ('rwnd', c_uint, 16),
        ('checksum', c_uint, 16),
        ('urgent_pointer', c_uint, 16),
        ('data', c_byte * MSS)  # array of MSS bytes
    ]

    def dump_contents(self):
        print 'src_port:', self.src_port
        print 'dst_port:', self.dst_port
        print 'seq_num:', self.seq_num
        print 'ack_num:', self.ack_num
        print 'hdr_len:', self.hdr_len
        print 'unused:', self.unused
        print 'URG:', self.URG
        print 'ACK:', self.ACK
        print 'PSH:', self.PSH
        print 'RST:', self.RST
        print 'SYN:', self.SYN
        print 'FIN:', self.FIN
        print 'rwnd:', self.rwnd
        print 'checksum:', self.checksum
        print 'urgent_pointer:', self.urgent_pointer
        print 'data:', self.get_payload()

    def get_data(self):
        return buffer(self)[:]

    def get_payload(self):
        return buffer(self.data)[:]

    def flag_string(self):
        flags = []
        if self.URG:
            flags.append('URG')
        if self.ACK:
            flags.append('ACK')
        if self.PSH:
            flags.append('PSH')
        if self.RST:
            flags.append('RST')
        if self.SYN:
            flags.append('SYN')
        if self.FIN:
            flags.append('FIN')
        return ' '.join(flags)

    def log_string(self):
        return '{},{},{},{},{},[{}]'.format(
            time.strftime('%m-%d-%yT%H:%M:%S'),
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            self.flag_string()
        )


def make_segment(src_port, dst_port, seq_num, ack_num,
        ACK=0, SYN=0, FIN=0, rwnd=0, data=''):
    segment = TCPSegment()
    segment.src_port = src_port
    segment.dst_port = dst_port
    segment.seq_num = seq_num
    segment.ack_num = ack_num
    segment.hdr_len = 20
    segment.unused = 0 # not implemented
    segment.URG = 0 # not implemented
    segment.ACK = ACK
    segment.PSH = 0 # not implemented
    segment.RST = 0 # not implemented
    segment.SYN = SYN
    segment.FIN = FIN
    segment.rwnd = rwnd
    segment.checksum = util.checksum(data)
    segment.urgent_pointer = 0 # not implemented
    memmove(addressof(segment.data), data, min(len(data), MSS))
    return segment


def rebuild_segment(data):
    segment = TCPSegment()
    memmove(addressof(segment), data, min(len(data), sizeof(segment)))
    return segment


if __name__ == '__main__':
    fd = open('bytes', 'rb')
    data = fd.read()
    fd.close()
    segments = make_payload_segments(data)
    for key, segment in segments.items():
        print key, segment, segment.get_payload()
        print len(list(buffer(segment)[:]))
