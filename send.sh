#!/bin/sh

REMOTE_PORT=41192
REMOTE_IP='209.2.219.180'
DIRECT_PORT=5000

ACK_PORT=6000

WINDOW_SIZE=4

test_small_file() {
    python sender.py test/test.txt $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test_medium_file() {
    python sender.py test/test.pdf $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test_large_file() {
    python sender.py test/test.mp3 $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test_direct() {
    python sender.py test/test.pdf $REMOTE_IP $DIRECT_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test_medium_file
