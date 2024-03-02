#!/bin/bash

sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo usermod -aG docker $USER
sudo apt install python3-pip -y

cd ~/ttds-data-collection
sudo docker-compose up -d
