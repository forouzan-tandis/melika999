#!/bin/bash 


ssh  mehdi@10.1.32.66  tar cvzf /tmp/haproxy-backup-$(date +%F)_.tar.gz /etc/haproxy
scp mehdi@10.1.32.66:/tmp/haproxy-backup-$(date +%F)_.tar.gz /backup/Captive/haproxy
ssh  mehdi@10.1.32.66  rm  /tmp/haproxy-backup-$(date +%F)_.tar.gz 



find   /backup/Captive/haproxy/  -iname haproxy* -mtime +30 -delete 
