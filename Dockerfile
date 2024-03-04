# Use NGINX as the base image
FROM nginx

# Install Python 3.5 and create virtual environment
RUN apt-get update && \
    apt-get install -y python3.5 python3-venv && \
    python3.5 -m venv /venv

# Set the PATH environment variable to include the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy your files and directories
COPY index.html /usr/share/nginx/html/
COPY . .

# Install required Python modules using pip
RUN pip install -r requirements.txt

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
