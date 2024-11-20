# Use a lightweight base image of Python
FROM python:3.9-slim

# Update and install security-related packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential libssl-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user with limited permissions
RUN useradd -m myuser
USER myuser

# Set the working directory
WORKDIR /home/myuser

# Copy the script and requirements to the container
COPY --chown=myuser:myuser main.py .
COPY --chown=myuser:myuser requirements.txt .

# Install dependencies in a virtual environment to minimize risk
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Command to run the script
ENTRYPOINT ["venv/bin/python", "main.py"]