#!/bin/sh

REMOTE_PORT=41192
REMOTE_IP='209.2.219.180'
ACK_PORT=6000
DIRECT_PORT=5000
WINDOW_SIZE=4

test1() {
    python sender.py test/test.txt $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test2() {
    python sender.py test/test.pdf $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test3() {
    python sender.py test/test.mp3 $REMOTE_IP $REMOTE_PORT $ACK_PORT stdout $WINDOW_SIZE
}

test4() {
    python sender.py test/test.mp3 $REMOTE_IP $DIRECT_PORT $ACK_PORT stdout $WINDOW_SIZE
}

run() {
    if [ $# -eq 1 ]; then
        if [ $1 = 1 ]; then
            test1
        elif [ $1 = 2 ]; then
            test2
        elif [ $1 = 3 ]; then
            test3
        elif [ $1 = 4 ]; then
            test4
        fi
    fi
}

if [ $# -eq 1 ]; then
    run $1
fi
