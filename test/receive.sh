#!/bin/sh

RECEIVER=../receiver.py

LISTENING_PORT=41194

SENDER_IP='209.2.219.180'
SENDER_PORT=6000

DIRECT_PORT=5000

test_small_file() {
    rm -f copy.txt
    python $RECEIVER copy.txt $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test.txt copy.txt
}

test_medium_file() {
    rm -f copy.pdf
    python $RECEIVER copy.pdf $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test.pdf copy.pdf
}

test_large_file() {
    rm -f copy.mp3
    python $RECEIVER copy.mp3 $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
    diff test.mp3 copy.mp3
}

test_direct() {
    rm -f copy.mp3
    python $RECEIVER copy.pdf $DIRECT_PORT $SENDER_IP $SENDER_PORT stdout
    diff test.pdf copy.pdf
}

test_medium_file
