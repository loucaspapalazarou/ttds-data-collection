#!/bin/bash

sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo usermod -aG docker $USER
sudo apt install python3-pip -y

# Check if .env file exists, if not, copy .env.example to .env
if [ ! -f .env ]; then
    cp .env.example .env
fi