#!/bin/bash

# Change to the GPU device directory
cd /sys/devices/57000000.gpu/devfreq/57000000.gpu/

# Check if all required parameters are provided
if [ -z "$1" ]; then
    echo "Error: Please provide delay time."
    exit 1
fi

# Assign input parameter to variable
delay=$1

# Define the list of possible frequencies
frequencies=('76800000' '153600000' '230400000' '307200000' '384000000' '460800000' '537600000' '614400000' '691200000' '768000000' '844800000' '921600000')

# Set the frequency governor to userspace
echo userspace > governor

# Loop to adjust frequency
while true; do
    # Generate a random number between 1 and 100
    random_num=$(( ( RANDOM % 100 ) + 1 ))

    # Check if the random number is less than or equal to 5
    if [ $random_num -le 5 ]; then
        # Randomly select a frequency from the list
        new_freq=${frequencies[$(( RANDOM % ${#frequencies[@]} ))]}

        # Read the current frequency
        current_frequency=$(cat cur_freq)

        # Compare current frequency with the new frequency
        if [ "$current_frequency" -ge "$new_freq" ]; then
            # If current frequency is higher than or equal to the new frequency,
            # adjust min_freq and max_freq
            echo "$new_freq" > min_freq 2>/dev/null
            echo "$new_freq" > max_freq 2>/dev/null
            direction="down"
        else
            # If current frequency is lower than the new frequency,
            # adjust max_freq first, then min_freq
            echo "$new_freq" > max_freq
            echo "$new_freq" > min_freq
            direction="up"
        fi

        # Print the current state for debugging or verification
        echo "Frequency changed $direction to $new_freq with delay $delay seconds."
    else
        # Read the current frequency
        current_frequency=$(cat cur_freq)

        # Print the current state for debugging or verification
        echo "No frequency change with delay $delay seconds."
    fi

    # Wait for the specified delay before next change
    sleep $delay

done
