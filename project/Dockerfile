# Use the official httpd base image
FROM httpd:latest

# Install Python, pip3, and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip3 install termcolor pymysql flask

# Set working directory
WORKDIR /var/www/html

# Copy your web application code to the container
COPY . .

# Expose port 80 for httpd
EXPOSE 80

# Start Apache HTTP Server
CMD ["httpd-foreground"]
