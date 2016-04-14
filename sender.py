from collections import OrderedDict
from segment import deserialize, serialize
from select import select
import socket
from sys import argv
import util

MSS = 576


class Sender:

    def __init__(self, filename, remote_ip, remote_port, ack_port,
            log_filename, window_size):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_addr = remote_ip, remote_port

        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_addr = 'localhost', ack_port
        self.recv_sock.bind(self.recv_addr)

        self.file = util.open_read_file(filename)
        self.log_file = util.open_write_file(log_filename)

        self.window_size = window_size

        self.seq_num = 0
        self.ack_num = 0

        self.sample_rtt = 0
        self.estimated_rtt = 0
        self.dev_rtt = 0

        self.timer_start = float('inf')
        self.timeout_interval = 3

        self.segments_in_transit = OrderedDict()
        self.segments_acked = set()

        self.inputs = [self.recv_sock, self.file]

    def done_sending(self):
        return self.file.closed and not self.segments_in_transit

    def update_stats(self):
        self.sample_rtt = util.current_time() - self.timer_start
        self.estimated_rtt = 0.875 * self.estimated_rtt + 0.125 * self.sample_rtt
        self.dev_rtt = 0.75 * self.dev_rtt + 0.25 * abs(
            self.sample_rtt - self.estimated_rtt)
        self.timeout_interval = self.estimated_rtt + 4 * self.dev_rtt

    def timeout(self):
        return util.current_time() - self.timer_start > self.timeout_interval

    def process_file(self):
        if len(self.segments_in_transit) >= self.window_size:
            return
        payload = self.file.read(MSS)
        if not payload:
            self.file.close()
            self.inputs.remove(self.file)
        else:
            if self.timer_start == float('inf'):
                self.timer_start = util.current_time()
            header, segment = self.make_segment(payload=payload)
            self.send_sock.sendto(segment, self.send_addr)
            self.log(header)
            self.segments_in_transit[self.seq_num] = payload
            self.seq_num += len(payload)

    def process_ack(self):
        segment = self.recv_sock.recv(1024)
        if util.checksum(segment) != 0:
            return
        header, payload = deserialize(segment)
        if header.seq_num in self.segments_acked:
            return
        self.segments_acked.add(header.seq_num)
        self.segments_in_transit.pop(header.seq_num)
        if self.segments_in_transit:
            seq_num, _ = self.next_segment()
            if header.seq_num == seq_num:
                self.reset_timer()  # timer corresponds to first segment
            self.ack_num = seq_num
        else:
            self.ack_num += len(payload)
        self.update_stats()

    def next_segment(self):
        return self.segments_in_transit.iteritems().next()

    def retransmit(self):
        seq_num, payload = self.next_segment()
        header, segment = self.make_segment(
            seq_num=seq_num,
            payload=payload
        )
        self.send_sock.sendto(segment, self.send_addr)
        self.log(header)

    def reset_timer(self):
        self.timer_start = util.current_time()

    def resolve_timeout(self):
        self.retransmit()
        self.reset_timer()

    def run(self):
        while not self.done_sending():
            readables, _, _ = select(self.inputs ,[], [], 0)
            if self.timeout():
                self.resolve_timeout()
            for readable in readables:
                if readable == self.recv_sock:
                    self.process_ack()
                elif readable == self.file:
                    self.process_file()
        self.send_fin_segment()
        self.log_file.close()

    def send_fin_segment(self):
        header, segment = self.make_segment(FIN=1, payload=' ')
        self.send_sock.sendto(segment, self.send_addr)
        self.log(header)

    def make_segment(self, seq_num=None, FIN=0, payload=''):
        return serialize(
            self.src_port,
            self.dst_port,
            seq_num or self.seq_num,
            self.ack_num,
            FIN=FIN,
            payload=payload
        )

    def log(self, header):
        self.log_file.write('{},{},{},{},{},[{}],{}\n'.format(
            util.current_time_string(),
            header.src_port,
            header.dst_port,
            header.seq_num,
            header.ack_num,
            header.flag_string(),
            self.estimated_rtt
        ))

    @property
    def src_port(self):
        return self.recv_addr[1]

    @property
    def dst_port(self):
        return self.send_addr[1]


if len(argv) == 6 or len(argv) == 7:
    filename = argv[1]
    remote_ip = argv[2]
    remote_port = int(argv[3])
    ack_port = int(argv[4])
    log_filename = argv[5]
    window_size = int(argv[6]) if len(argv) == 7 else 1

    sender = Sender(filename, remote_ip, remote_port, ack_port, log_filename, window_size)
    sender.run()
else:
    print (
        'Usage: python {} <filename> <remote_IP> <remote_port> '
        '<ack_port_num> <log_filename> <window_size>'.format(argv[0])
    )
