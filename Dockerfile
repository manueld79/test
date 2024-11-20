# Use a secure slim Python base image
FROM python:3.9-slim-bullseye

# Update and install required security-related packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential libc-bin libssl-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Create a non-root user with limited permissions
RUN useradd -m -s /bin/bash myuser
USER myuser

# Set the working directory
WORKDIR /home/myuser

# Copy the script and requirements to the container
COPY --chown=myuser:myuser main.py .
COPY --chown=myuser:myuser requirements.txt .

# Use Python virtual environment to isolate dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Ensure proper file permissions
RUN chmod -R 700 /home/myuser && chown -R myuser:myuser /home/myuser

# Entry point
ENTRYPOINT ["venv/bin/python", "main.py"]