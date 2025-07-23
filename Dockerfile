# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app/src
COPY src/requirements.txt /app/src/

# Install the required packages
RUN pip install --no-cache-dir -r /app/src/requirements.txt

# Copy the rest of the application source code
COPY . /app

# Command to run when the container starts.
# It will automatically run the structured data extraction.
CMD ["python", "src/round1b.py"]