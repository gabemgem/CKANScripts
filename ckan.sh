#!/usr/bin/bash
# bash script for executing ckan commands at root level
# refer to http://docs.ckan.org/en/2.9/maintaining/cli.html for commands
docker exec -it -u 0 ckan /usr/local/bin/ckan -c /etc/ckan/production.ini $*