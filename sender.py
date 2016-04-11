from collections import OrderedDict
from segment import make_segment, MSS
import socket
import sys
import util


def send(filename, remote_address, ack_port, log_filename, window_size):
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ack_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ack_sock.bind(('localhost', ack_port))

    target_file = util.open_read_file(filename)
    log_file = util.open_write_file(log_filename)

    segments = OrderedDict() # fast index of segments, TODO: pop after ACK

    # TODO: implement timeout
    # TODO: implement window size
    seq_num, ack_num = 0, 0
    estimated_rtt = 100 # TODO: k&r 3.5.3
    segment_data = target_file.read(MSS)
    while segment_data:
        segment = make_segment(
            ack_port,
            remote_address[1],
            seq_num,
            ack_num,
            data=segment_data
        )
        segments[seq_num] = segment
        remote_sock.sendto(segment.get_data(), remote_address)
        log_file.write('{},{}\n'.format(segment.log_string(), estimated_rtt))
        seq_num += MSS
        segment_data = target_file.read(MSS)

    segment = make_segment(ack_port, remote_address[1], seq_num + 1, ack_num, FIN=1)
    remote_sock.sendto(segment.get_data(), remote_address)

    target_file.close()
    log_file.close()


if len(sys.argv) == 6 or len(sys.argv) == 7:
    filename = sys.argv[1]
    remote_address = sys.argv[2], int(sys.argv[3])
    ack_port = int(sys.argv[4])
    log_filename = sys.argv[5]
    window_size = int(sys.argv[6]) if len(sys.argv) == 7 else 1
    send(filename, remote_address, ack_port, log_filename, window_size)
else:
    print (
        'Usage: python {} <filename> <remote_IP> <remote_port> '
        '<ack_port_num> <log_filename> <window_size>'.format(sys.argv[0])
    )
