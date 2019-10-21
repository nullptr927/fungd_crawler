#!/bin/sh

echo "트게더 크롤러. 끝내려면 (Ctrl + c) 를 누르세요."

trap break INT

while true; do  
    python3 tchang.py
done

trap - INT

echo "Crawler Killed."
