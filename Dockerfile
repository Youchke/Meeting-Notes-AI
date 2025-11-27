# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (ffmpeg is required for pydub/moviepy)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add src to PYTHONPATH so that main.py can import pipelines
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Copy the rest of the application code
COPY . .

# Run main.py when the container launches
CMD ["python", "main.py"]
