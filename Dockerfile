# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for data
RUN mkdir /data

# Command to run the application
CMD ["python", "your_script.py"]