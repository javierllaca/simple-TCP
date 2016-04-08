import sys

if len(sys.argv) == 6:
    received_file = open(sys.argv[1], 'wb')
    listening_port = int(sys.argv[2])
    sender_ip = sys.argv[3]
    sender_port = int(sys.argv[4])
    log_file = open(sys.argv[5], 'wb')
else:
    print (
        'Usage: python {} <filename> <listening_port> <sender_IP> '
        '<sender_port> <log_filename>'.format(sys.argv[0])
    )
