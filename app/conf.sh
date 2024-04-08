#!/bin/bash

# Check the operating system
if [[ $(uname) == "Linux" ]]; then
    #export PUBLIC_IP=$(curl -s http://ifconfig.me/ip)
    echo "Linux Distribution of OPA service"
    export PUBLIC_IP=$(hostname -I | awk '{print $1}')
    echo $PUBLIC_IP

elif [[ $(uname) == "Darwin" ]]; then
    echo "Mac Distribution of OPA service"
    export PUBLIC_IP=$(ipconfig getifaddr en0)
    echo $PUBLIC_IP
elif [[ $(uname) == "MINGW"* ]]; then
    echo "Windows Distribution of OPA service"
    export PUBLIC_IP=$(powershell.exe -Command "(Test-Connection -ComputerName (hostname) -Count 1).IPAddressToString")
    echo $PUBLIC_IP
else
    echo "Unsupported operating system, kakfa service might no be running properly"
    exit 1
fi

# Build Docker images
docker image build Extract_Stream -t stream_producer:latest
docker image build API -t opa_api:latest
docker image build Extract_Transform_Hist -t historic_handler:latest
docker image build  Load_Stream -t stream_loader:latest

# Start Docker containers using docker-compose
docker-compose up -d