FROM  python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set env path for db for prd 
ENV DB_PATH=/app/db/flashcards.db

# Copy the requirements file into the container
COPY requirements.txt .

# Create the db directory
RUN mkdir -p /app/db

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
