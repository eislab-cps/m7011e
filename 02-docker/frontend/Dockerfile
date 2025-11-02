# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy frontend files
COPY index.html .

# Expose port 8080
EXPOSE 8080

# Start Python HTTP server
CMD ["python3", "-m", "http.server", "8080"]
