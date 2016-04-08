import sys

if len(sys.argv) == 7:
    sent_file = open(sys.argv[1], 'rb')
    remote_ip = sys.argv[2]
    remote_port = int(sys.argv[3])
    ack_port = int(sys.argv[4])
    log_file = sys.argv[5]
    window_size = int(sys.argv[6])
else:
    print (
        'Usage: python {} <filename> <remote_IP> <remote_port> '
        '<ack_port_num> <log_filename> <window_size>'.format(sys.argv[0])
    )
