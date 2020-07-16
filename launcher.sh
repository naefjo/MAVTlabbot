#!/bin/zsh
conda activate Basic
echo "activated conda env"
docker_id=$(docker run -d -p 4545:4444 --shm-size 2g selenium/standalone-firefox)
echo "Docker ID of Selenium Image: $docker_id"
sleep 5s
echo "executing Labbot scrit. Interrupt it using Ctrl-C"
python labbot_main.py
echo "script interrupted stopping Docker Image"
docker kill $docker_id
docker ps
