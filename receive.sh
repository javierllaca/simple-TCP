#!/bin/sh

LISTENING_PORT=41194
SENDER_IP='209.2.219.180'
SENDER_PORT=6000
DIRECT_PORT=5000

test1 () {
    rm -f test/copy.txt
    python receiver.py test/copy.txt $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
}

test2() {
    rm -f test/copy.pdf
    python receiver.py test/copy.pdf $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
}

test3() {
    rm -f test/copy.mp3
    python receiver.py test/copy.mp3 $LISTENING_PORT $SENDER_IP $SENDER_PORT stdout
}

test4() {
    rm -f test/copy.mp3
    python receiver.py test/copy.mp3 $DIRECT_PORT $SENDER_IP $SENDER_PORT stdout
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
