from segment import rebuild_segment
import socket
import sys
import util


def receive(filename, listening_port, sender_address, log_filename):
    listening_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listening_sock.bind(('localhost', listening_port))
    sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    target_file = util.open_write_file(filename)
    log_file = util.open_write_file(log_filename)

    while True:
        data, addr = listening_sock.recvfrom(1024)
        segment = rebuild_segment(data)
        log_file.write('{}\n'.format(segment.log_string()))
        # TODO: send ACK
        if segment.FIN:
            break
        for byte in segment.get_payload():
            if ord(byte):
                target_file.write(byte)
            else:
                break

    target_file.close()
    log_file.close()


if len(sys.argv) == 6:
    filename = sys.argv[1]
    listening_port = int(sys.argv[2])
    sender_address = sys.argv[3], int(sys.argv[4])
    log_filename = sys.argv[5]
    receive(filename, listening_port, sender_address, log_filename)
else:
    print (
        'Usage: python {} <filename> <listening_port> <sender_IP> '
        '<sender_port> <log_filename>'.format(sys.sys.argv[0])
    )
