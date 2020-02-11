#!/bin/bash

# To integrate this script with the Inite project follow this steps:
#  NOTE: All paths must be completed
#
#   1. Make this file executable:
#      `chmod +x /path/to/psql.sh`
#
#   2. Change file owner and group to the postgres user:
#      `chown postgres:postgres /path/to/psql.sh`
#
#   3. Set the cron job that will execute this script on start up and in schedul:
#      sudo -u postgres bash
#      (crontab -l 2>/dev/null; echo  "30 14 * * * /path/to/psql.sh") | crontab -
#      (crontab -l 2>/dev/null; echo  "@reboot /path/to/psql.sh") | crontab -


DB_NAME=$(sed -n 's/"DB_NAME"[\ :"]*\([^,"]*\)\(.*\)/\1/p' /etc/inite/variables.json)
psql -d $DB_NAME -c "delete from portal_registre";
