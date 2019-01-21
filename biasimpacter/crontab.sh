#!/usr/bin/env bash

# Ensure the log file exists
touch /var/log/crontab.log

# Ensure permission on the command
chmod a+x /usr/bin/python

# Added a cronjob in a new crontab
# Warning: 
# crontab uses its own env, you need to export .env file so script
# can access variables
echo "* * * * * export $(cat /biasimpacter/.env | xargs); cd /biasimpacter/biasimpacter && /usr/local/bin/python /biasimpacter/biasimpacter/app/app.py >> /var/log/crontab.log 2>&1
" > /etc/crontab

# Registering the new crontab
crontab /etc/crontab

# Starting the cron
/usr/sbin/service cron start

# Displaying logs
# Useful when executing docker-compose logs mycron
tail -f /var/log/crontab.log
