# Use NGINX as the base image
FROM nginx

# Install Python 3.5 and pip
RUN apt-get update && apt-get install -y \
    python3.5 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY index.html /usr/share/nginx/html/
# Copy the Python script into the container
COPY . .

# Install required Python modules using pip
RUN pip install -vvv python-jenkins requests Jinja2

# Copy the cron job file into the container
COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Apply cron job
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && nginx -g 'daemon off;'
