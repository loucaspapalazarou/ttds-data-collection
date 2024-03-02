#!/bin/bash

sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo usermod -aG docker $USER
sudo apt install python3-pip -y
sudo docker-compose up -d -f ~/ttds-data-collection/docker-compose.yml
