#!/bin/sh

IP='209.2.219.180'

test1() {
    newudpl-1.4/newudpl -vv -i $IP':*' -o $IP
}

test2() {
    newudpl-1.4/newudpl -vv -i $IP':*' -o $IP -B 1 -L 1 -O 1
}

test3() {
    newudpl-1.4/newudpl -vv -i $IP':*' -o $IP -B 2 -L 2 -O 2
}

test2
