#!/bin/bash


cd /sys/devices/57000000.gpu/devfreq/57000000.gpu/

#Check if an input parameter is provided
if [ -z "$1" ]; then
echo "Error: Please provide an input parameter."
exit 1
fi

# Assign the provided frequency parameter to a variable
frequency="$1"


echo userspace > governor

# Read the current frequency from the cur_freq file
current_frequency=$(cat cur_freq)

# Compare the current frequency with the provided frequency parameter
if [ "$current_frequency" -ge "$frequency" ]; then
    # If current frequency is equal or higher than the parameter frequency
    echo "$frequency" > min_freq
    echo "$frequency" > max_freq
else
    # If current frequency is lower than the parameter frequency
    echo "$frequency" > max_freq
    echo "$frequency" > min_freq
fi




