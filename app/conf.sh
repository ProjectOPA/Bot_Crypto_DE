#!/bin/bash

# Check the operating system
if [[ $(uname) == "Linux" ]]; then
    # If on Linux, set PUBLIC_IP using curl
    #export PUBLIC_IP=$(curl -s http://ifconfig.me/ip)
    echo "Linux Distribution of OPA service"
    export PUBLIC_IP=$(hostname -I | awk '{print $1}')
    echo $PUBLIC_IP

elif [[ $(uname) == "Darwin" ]]; then
    # If on macOS, set PUBLIC_IP using ipconfig
    echo "Mac Distribution of OPA service"
    export PUBLIC_IP=$(ipconfig getifaddr en0)
    echo $PUBLIC_IP
elif [[ $(uname) == "MINGW"* ]]; then
    # If on Windows (using Git Bash or similar), set PUBLIC_IP using PowerShell
    echo "Windows Distribution of OPA service"
    export PUBLIC_IP=$(powershell.exe -Command "(Test-Connection -ComputerName (hostname) -Count 1).IPAddressToString")
    echo $PUBLIC_IP
else
    # Handle other operating systems here if needed
    echo "Unsupported operating system, kakfa service might no be running properly"
    exit 1
fi

# Build Docker images
docker image build Extract_Stream -t stream_producer:latest
docker image build API -t opa_api:latest
docker image build Extract_Transform_Hist -t historic_handler:latest
docker image build  Load_Stream -t stream_loader:latest

# Start Docker containers using docker-compose
docker-compose up --scale kafka=2 -d