from ctypes import addressof, c_uint, memmove, sizeof, Structure
import util


class TCPSegmentHeader(Structure):

    _fields_ = [
        ('src_port', c_uint, 16),
        ('dst_port', c_uint, 16),
        ('seq_num', c_uint, 32),
        ('ack_num', c_uint, 32),
        ('hdr_len', c_uint, 4),
        ('unused', c_uint, 6),  # not implemented
        ('URG', c_uint, 1),  # not implemented
        ('ACK', c_uint, 1),
        ('PSH', c_uint, 1),  # not implemented
        ('RST', c_uint, 1),  # not implemented
        ('SYN', c_uint, 1),
        ('FIN', c_uint, 1),
        ('rwnd', c_uint, 16),  # not implemented
        ('checksum', c_uint, 16),
        ('urgent_pointer', c_uint, 16),  # not implemented
    ]

    def serialize(self):
        return buffer(self)[:]

    def __len__(self):
        return sizeof(self)

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

    def __str__(self):
        return '\n'.join([
            'src_port: {}'.format(self.src_port),
            'dst_port: {}'.format(self.dst_port),
            'seq_num: {}'.format(self.seq_num),
            'ack_num: {}'.format(self.ack_num),
            'hdr_len: {}'.format(self.hdr_len),
            'flags: [{}]'.format(self.flag_string()),
            'checksum: {}'.format(self.checksum),
            'urgent_pointer: {}'.format(self.urgent_pointer)
        ])


def serialize(src_port, dst_port, seq_num, ack_num,
        ACK=0, SYN=0, FIN=0, payload=''):
    header = TCPSegmentHeader()
    header.src_port = src_port
    header.dst_port = dst_port
    header.seq_num = seq_num
    header.ack_num = ack_num
    header.hdr_len = 5  # 20 bytes in 32-bit words
    header.ACK = ACK
    header.SYN = SYN
    header.FIN = FIN
    header.checksum = util.checksum(header.serialize() + payload)
    return header, header.serialize() + payload


def deserialize(segment):
    header = TCPSegmentHeader()
    header_data, payload = segment[:len(header)], segment[len(header):]
    memmove(addressof(header), header_data, len(header))
    return header, payload
