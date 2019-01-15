FROM python:3.6
RUN apt-get update -y
RUN apt-get install -y cron
COPY . /biasimpacter
WORKDIR /biasimpacter
RUN pip install -r requirements.txt

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/biasimpact-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/biasimpact-cron

# Apply cron job
RUN crontab /etc/cron.d/biasimpact-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
