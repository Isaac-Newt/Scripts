#!/bin/bash

# Copyright 2020 - Isaac List
# Licensed under the MIT license

# A script to check network connectivity every second.
# Will run indefinitely, and save to a new log file at
# set intervals.

# Initialize counter for log files
file_number=1

while true;
do
    # Count of timestamp/exit code logs
    count=1

    # While less than desired number of seconds (3600/hr)
    while [ $count -le 10 ];
    do
        # Get exit code and timestamp
        check=`ping -c 1 google.com`
        success=$?
        timestamp=`date '+%a %m-%d-%Y %T'`
        
        # Write to log file in script directory
        echo "$timestamp, $success" >> $file_number.csv;
    sleep 1;
    
    # Record how many seconds
    ((count++))
    done

    # Increment log file name
    ((file_number++))
done
