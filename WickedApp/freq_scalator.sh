#!/bin/bash

# Change to the GPU device directory
cd /sys/devices/57000000.gpu/devfreq/57000000.gpu/

# Check if all required parameters are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
	echo "Error: Please provide minimum frequency, maximum frequency, and delay time."
	 exit 1
fi

# Assign input parameters to variables
min_freq=$1
max_freq=$2
delay=$3

# Set the frequency governor to userspace
echo userspace > governor

flag=0

# Loop to adjust frequency
while true; do
	if [ $flag -eq 1 ]; then 
		new_freq=$min_freq
	else
		new_freq=$max_freq	
	fi
	
	# Toggle flag
	if [ $flag -eq 1 ]; then	    
		flag=0	    
	else	        
		flag=1		
	fi
	
	# Read the current frequency
	current_frequency=$(cat cur_freq)
			   
	# Compare the current frequency with the provided frequency parameters			        
	if [ "$current_frequency" -ge "$new_freq" ]; then
				
		# If current frequency is higher than or equal to min_freq, adjust max and min frequencies					        
		echo "$new_freq" > min_freq 2>/dev/null				        
		echo "$new_freq" > max_freq 2>/dev/null
								    
	else
									            
		# If current frequency is lower than min_freq, adjust max and min frequencies									            
		echo "$new_freq" > max_freq
		echo "$new_freq" > min_freq
												        
	fi
													    
													    
	# Print the current state for debugging or verification
													        
	echo "Current frequency set to $new_freq with delay $delay seconds."
														    
	# Wait for the specified delay before next change
	sleep $delay

done
