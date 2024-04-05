# Utilize an appropriate base image
FROM ubuntu:latest

# Upgrade pip and install dependencies
RUN apt-get update && apt-get install python3-pip -y

# Setting default work directory
WORKDIR /application

# Copy all the required files into the container
ADD . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

# Command to execute the script
CMD ["uvicorn", "api:api", "--reload", "--host", "0.0.0.0"]