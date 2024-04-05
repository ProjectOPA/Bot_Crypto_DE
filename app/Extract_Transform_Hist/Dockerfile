# Utilize an appropriate base image
FROM ubuntu:latest

# Upgrade pip and install dependencies
RUN apt-get update && apt-get install python3-pip -y && apt-get -y install cron

# Setting default work directory
WORKDIR /application

# Copy all the required files into the container
ADD . .

RUN pip3 install -r requirements.txt && chmod +x main.sh

# Command to execute the script for the extraction
CMD ["./main.sh"]