#!/usr/bin/env bash
cd HRMS/
git pull origin dev
sudo export DOCKER_BUILDKIT=0
sudo docker-compose up --build -d



