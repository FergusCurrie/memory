FROM  python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set env path for db for prd 
ENV DB_PATH=/app/db/flashcards.db

# Install some stuff 
RUN apt-get update && apt-get install -y \
    sqlite3 



# Copy the requirements file into the container
COPY requirements.txt .

# Create the db directory
RUN mkdir -p /app/db

# Install spark
RUN mkdir -p /etc/apt/keyrings
RUN wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
RUN echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
RUN apt-get update && apt-get install -y temurin-17-jdk
ENV JAVA_HOME /usr/lib/jvm/temurin-17-jdk-arm64


# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# COPY backend backend
# COPY static static
COPY . . 
# COPY static .
# COPY backend . 


# Expose the port the app runs on
EXPOSE 9898

# Command to run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "9898"]
