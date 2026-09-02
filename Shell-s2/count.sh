#!/usr/bin/env bash

count=0

while [ "$count" -lt 5 ]; do
    echo "This is iteration number $count"
    ((count++))
done