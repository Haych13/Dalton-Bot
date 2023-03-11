# Use an official Python runtime as the base image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and directories into the container
COPY main.py .
COPY .env .
COPY daltonize.py .
COPY daltonized/ .
COPY simulated/ .

#Add a label
LABEL "dalton-bot"=""

# Define the command to run when the container starts
CMD ["python", "-u","main.py"]

