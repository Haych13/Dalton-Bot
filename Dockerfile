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
COPY daltonize.py .
COPY daltonized/ .
COPY simulated/ .

#Add a label
LABEL "dalton-bot"=""

# Define the command to run when the container starts
CMD ["python", "-u", "main.py"]

# Set environment variables
ENV USERNAME=$USERNAME
ENV PASSWORD=$PASSWORD
ENV CLIENT_ID=$CLIENT_ID
ENV CLIENT_SECRET=$CLIENT_SECRET
ENV IMGUR_CLIENT_ID=$IMGUR_CLIENT_ID
ENV FOOTER_TEXT=$FOOTER_TEXT
ENV D_OUTPUT_DIR_DEUTERANOPIA=$D_OUTPUT_DIR_DEUTERANOPIA
ENV D_OUTPUT_DIR_PROTANOPIA=$D_OUTPUT_DIR_PROTANOPIA
ENV D_OUTPUT_DIR_TRITANOPIA=$D_OUTPUT_DIR_TRITANOPIA
ENV S_OUTPUT_DIR_DEUTERANOPIA=$S_OUTPUT_DIR_DEUTERANOPIA
ENV S_OUTPUT_DIR_PROTANOPIA=$S_OUTPUT_DIR_PROTANOPIA
ENV S_OUTPUT_DIR_TRITANOPIA=$S_OUTPUT_DIR_TRITANOPIA
