@echo off

REM Stop and remove the Docker container
docker stop awm_django_pwa
docker rm awm_django_pwa

REM Remove the Docker image
docker rmi awm_project_pwa:latest

REM Rebuild the Docker image
docker build -t awm_project_pwa .

REM Build the Docker container
docker create --name awm_django_pwa --network awm_network --network-alias awm_django_alias -t -p 8001:8001 awm_project_pwa

REM Start the Docker container
docker start awm_django_pwa