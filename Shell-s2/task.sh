#!/bin/bash

mkdir task
cd task
echo "Current Date: $(date)"> task.log
# process
echo "Process : $(ps) ">> task.log
# hostname and username
echo "Hostname: $(hostname) and username $(whoami)" >> task.log

# add process info inside a file name process.log
echo "Process Info: $(ps )" > process.log
echo "disk usage: $(df -h)" >> process.log








