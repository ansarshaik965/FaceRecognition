# Use an official Python runtime as a parent image
FROM python:3.9.18-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    libjpeg-dev \
    zlib1g-dev

# Expose port 80 to the outside world
EXPOSE 80

# Copy the Apache2 configuration file
COPY apache2.conf /etc/apache2/sites-available/000-default.conf

RUN apachectl restart

# Start Apache2
CMD ["apache2ctl", "-D", "FOREGROUND"]
