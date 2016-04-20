from heapq import heappop, heappush
from segment import deserialize, serialize
from select import select
import socket
from sys import argv
import util


class Receiver:

    def __init__(self, filename, listening_port, sender_ip, sender_port,
            log_filename):
        sender_ip, sock_family = util.addr_family(sender_ip, sender_port)

        self.send_sock = socket.socket(sock_family, socket.SOCK_DGRAM)
        self.send_addr = sender_ip, sender_port

        self.recv_sock = socket.socket(sock_family, socket.SOCK_DGRAM)
        self.recv_addr = socket.gethostname(), listening_port
        self.recv_sock.bind(self.recv_addr)

        self.file = util.open_write_file(filename)
        self.log_file = util.open_write_file(log_filename)

        self.seq_num = 0
        self.ack_num = 0

        self.ACK = 0

        self.bytes_received = 0

        self.segments_acked = set()
        self.pending = []

        self.done = False

        self.inputs = [self.recv_sock]

    def run(self):
        while not self.done:
            readables, _, _ = select(self.inputs ,[], [], 0)
            for readable in readables:
                if readable == self.recv_sock:
                    self.process_segment()
        self.close()

    def process_segment(self):
        segment = self.recv_sock.recv(1024)
        if util.checksum(segment) != 0:
            return
        header, payload = deserialize(segment)
        self.log(header)
        self.seq_num = header.seq_num
        ack = header.seq_num + len(payload)
        if ack in self.segments_acked:
            return
        self.bytes_received += len(payload)
        self.segments_acked.add(ack)
        self.ACK = 1 if header.seq_num == self.ack_num else 0
        ack_header, ack_segment = self.make_segment(payload, header.FIN)
        self.send_sock.sendto(ack_segment, self.send_addr)
        if header.FIN:
            self.done = True
            return
        self.store_payload(header.seq_num, payload)
        seq_num, payload = self.fetch_next_payload()
        while seq_num == self.ack_num:
            self.file.write(payload)
            self.ack_num += len(payload)
            self.pop_next_payload()
            seq_num, payload = self.fetch_next_payload()

    def pop_next_payload(self):
        return heappop(self.pending)

    def fetch_next_payload(self):
        if self.pending:
            return self.pending[0]
        return None, None

    def store_payload(self, seq_num, payload):
        heappush(self.pending, (seq_num, payload))

    def close(self):
        print 'Delivery completed successfully'
        print 'Received {} bytes'.format(self.bytes_received)
        self.file.close()
        self.log_file.close()

    def make_segment(self, payload, FIN):
        return serialize(
            self.src_port,
            self.dst_port,
            self.seq_num,
            self.ack_num,
            payload=payload,
            FIN=FIN
        )

    def log(self, header):
        self.log_file.write('{},{},{},{},{},[{}]\n'.format(
            util.current_time_string(),
            header.src_port,
            header.dst_port,
            header.seq_num,
            header.ack_num,
            header.flag_string()
        ))

    @property
    def src_port(self):
        return self.recv_addr[1]

    @property
    def dst_port(self):
        return self.send_addr[1]


if len(argv) == 6:
    filename = argv[1]
    listening_port = int(argv[2])
    sender_ip = argv[3]
    sender_port = int(argv[4])
    log_filename = argv[5]

    receiver = Receiver(filename, listening_port, sender_ip, sender_port, log_filename)
    receiver.run()
else:
    print (
        'Usage: python {} <filename> <listening_port> <sender_IP> '
        '<sender_port> <log_filename>'.format(argv[0])
    )
