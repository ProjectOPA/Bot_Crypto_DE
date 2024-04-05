#!/bin/bash
docker image build Extract_Stream -t stream_producer:latest
docker image build API -t opa_api:latest
docker image build Extract_Transform_Hist -t historic_handler:latest
docker image build  Load_Stream -t stream_loader:latest
docker-compose up --scale kafka=2 -d