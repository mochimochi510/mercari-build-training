FROM python:3.9-alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari

# Set the working directory
WORKDIR /app

# Install SQLite and other dependencies
RUN apk add --no-cache sqlite

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app

# Change ownership of the application directory
RUN chown -R trainee:mercari /app

RUN chown -R trainee:mercari /path/to/db

USER trainee

# Expose the port the app runs on
EXPOSE 9050

# Run the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9050"]