# Simple TCP

A simple TCP-like transport layer protocol

## Running

Three programs must be run at the same time: the sender, receiver, and a link emulator over UDP.

### Link emulator

    newudpl-1.4/newudpl -vv -i '127.0.0.1:*'

### Sender

    python sender.py <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename> <window_size>
    python sender.py file.txt localhost 41192 6000 logfile.txt 1152

### Receiver

    python receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>
    python receiver.py file.txt 41194 localhost 6000 [log.txt]
