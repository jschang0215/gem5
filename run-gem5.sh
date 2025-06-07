#!/bin/bash

# === Configuration ===
IMAGE="ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0"
CONTAINER_NAME="gem5-docker"
HOST_GEM5_DIR="$HOME/Desktop/gem5"
CONTAINER_GEM5_DIR="/home/gem5"

# === Pull the latest image ===
echo "[INFO] Pulling gem5 Docker image..."
docker pull "$IMAGE"

# === Check if the container already exists ===
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "[INFO] Starting existing container: $CONTAINER_NAME"
    docker start -ai "$CONTAINER_NAME"
else
    echo "[INFO] Creating and running new container: $CONTAINER_NAME"
    docker run -it \
        --name "$CONTAINER_NAME" \
        -v "$HOST_GEM5_DIR":"$CONTAINER_GEM5_DIR" \
        "$IMAGE"
fi
