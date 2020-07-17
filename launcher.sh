#!/bin/zsh
conda activate Basic
echo "activated conda env"
if [[ "$1" != "local" ]]; then
	docker_id=$(docker run -d -p 4545:4444 --shm-size 2g selenium/standalone-firefox)
	echo "Docker ID of Selenium Image: $docker_id"
else
	echo "starting script locally without docker"
fi
sleep 5s
echo "executing Labbot scrit. Interrupt it using Ctrl-C"
python labbot_main.py $1
echo "script interrupted"
if [[ "$1" != "local" ]]; then
	echo "stopping docker"
	docker stop $docker_id
	docker rm $docker_id
fi
docker ps
