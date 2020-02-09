#!/bin/bash

# To integrate this script with the Inite project follow this steps:
#   
#   1. Make this file executable:
#      `chmod +x /path/to/psql.sh`
#
#   2. Change file owner and group to the postgres user:
#      `chown postgres:postgres /path/to/psql.sh`
#
#   3. Set the cron job that will execute this file:
#      `(crontab -l 2>/dev/null; echo  "* * * * * /path/to/psql.sh") | crontab -`
`      
#
#   4. Make this script to execute on start up:
#   


DB_NAME=$(sed -n 's/"DB_NAME"[\ :"]*\([^,"]*\)\(.*\)/\1/p' /etc/inite/variables.json)
psql -d $DB_NAME -c "delete from portal_registre";
