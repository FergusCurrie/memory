#!/bin/bash

# Set variables
SPARK_VERSION=3.3.0
HADOOP_VERSION=3
JAVA_VERSION=11.0.11+9

# Install wget to download Java
apt-get update
apt-get install -y wget
rm -rf /var/lib/apt/lists/*

# Download OpenJDK
OPENJDK_URL="https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.11%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.11_9.tar.gz"
OPENJDK_TAR="OpenJDK11U-jdk_x64_linux_hotspot_11.0.11_9.tar.gz"

echo "Downloading OpenJDK..."
wget -q "$OPENJDK_URL" -O "$OPENJDK_TAR"

if [ ! -f "$OPENJDK_TAR" ]; then
    echo "Failed to download OpenJDK"
    exit 1
fi

# Extract OpenJDK
tar -xzf "$OPENJDK_TAR"

# Move extracted directory
mv jdk-11.0.11+9 /usr/local/

# Clean up
rm "$OPENJDK_TAR"
