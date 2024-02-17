# Dockerfile
FROM python:3.9-slim

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set the working directory in the container
WORKDIR /app

# Copy the entire app directory to the working directory in the container
COPY ./app .

# Install dependencies
RUN pip install -r requirements.txt

# Command to run on container start
CMD ["streamlit", "run", "app.py"]

