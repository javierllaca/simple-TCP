#!/bin/sh

LISTENING_PORT=41194

SENDER_IP='209.2.219.180'
SENDER_PORT=6000

DIRECT_PORT=5000

test_small_file() {
    rm -f test/copy.txt
    python receiver.py test/copy.txt $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test/test.txt test/copy.txt
}

test_medium_file() {
    rm -f test/copy.pdf
    python receiver.py test/copy.pdf $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test/test.pdf test/copy.pdf
}

test_large_file() {
    rm -f test/copy.mp3
    python receiver.py test/copy.mp3 $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test/test.mp3 test/copy.mp3
}

test_direct() {
    rm -f test/copy.mp3
    python receiver.py test/copy.pdf $DIRECT_PORT $SENDER_IP $SENDER_PORT stdout
    diff test/test.pdf test/copy.pdf
}

test_medium_file
