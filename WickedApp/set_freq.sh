
#!/bin/bash

# Change to the GPU device directory
cd /sys/devices/57000000.gpu/devfreq/57000000.gpu/

# Check if the required parameter is provided
if [ -z "$1" ]; then
	    echo "Error: Please provide a frequency."
	        exit 1
	fi

	# Assign input parameter to variable
	new_freq=$1

	# Set the frequency governor to userspace
	echo userspace > governor

	# Read the current frequency
	current_frequency=$(cat cur_freq)

	# Compare the current frequency with the provided frequency parameter
	if [ "$current_frequency" -ge "$new_freq" ]; then
		    # If current frequency is higher than or equal to new_freq, adjust max and min frequencies
		        echo "$new_freq" > min_freq 
			    echo "$new_freq" > max_freq
		    else
			        # If current frequency is lower than new_freq, adjust max and min frequencies
				    echo "$new_freq" > max_freq
				        echo "$new_freq" > min_freq
				fi

				# Print the current state for debugging or verification
				echo "Frequency set to $new_freq."


