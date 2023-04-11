# Use the official Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Install Docker
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-transport-https ca-certificates curl gnupg lsb-release && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code into the container
COPY . .

# Create a volume for the /tmp/lambdapi/files directory
VOLUME ["/tmp/lambdapi/files"]

# Expose the FastAPI application's port (8000) to the outside world
EXPOSE 8000

# Start the FastAPI application using single Uvicorn server
# CMD ["python", "main.py"]

# TO RUN MORE WORKERS IN PRODUCTION USE THIS
CMD ["sh", "-c", "gunicorn -w $(nproc) --timeout 360 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app"]
