#!/bin/sh

echo "트게더 크롤러. 끝내려면 (Ctrl + c) 를 누르세요."

sed "s/dir1 = ''  # 경로를 설정해 주세요/dir1 = '/output/output.txt'  # 경로를 설정해 주세요" ./tchang.py

trap break INT

while true; do  
    python3 tchang.py
done

trap - INT

echo "Crawler Killed."
