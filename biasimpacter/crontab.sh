
#!/usr/bin/env bash

# Ensure the log file exists
touch /biasimpacter/logs/crontab.log


# Added a cronjob in a new crontab
echo "0 10 * * * python /biasimpacter/app/app.py >> /biasimpacter/logs/crontab.log 2>&1" > /etc/crontab

# Registering the new crontab
crontab /etc/crontab

# Starting the cron
/usr/sbin/service cron start

# Displaying logs
# Useful when executing docker-compose logs mycron
tail -f /biasimpacter/logs/crontab.log