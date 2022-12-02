#!/usr/bin/bash
# bash script cleaning datasets without completely wiping the db (negates having to reinitialize)
docker exec -it -u 0 ckan /usr/local/bin/ckan -c /etc/ckan/production.ini dataset list > list.txt
tail -n +10 list.txt > list2.txt
cut -d' ' -f1 list2.txt > ids.txt
perl -ne 's/\e\[\d+m//g;print' < ids.txt > output.txt
python3 purge.py
rm list.txt
rm list2.txt
rm ids.txt
#rm output.txt