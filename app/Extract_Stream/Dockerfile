# Utilize an appropriate base image
FROM python:3.10-slim

# Setting default work directory
WORKDIR /application

# Copy all the required files into the container
ADD . .

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

# Command to execute the script for the extraction
CMD python3.10 producer_streaming.py