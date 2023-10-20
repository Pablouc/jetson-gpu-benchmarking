
OUTPUT_FILE="powerConsumption.txt"

# Fetch the readings from the specified paths
CURR1=$(cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon4/curr1_input)
IN1=$(cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon4/in1_input)

# Write the readings to the output file
echo "Timestamp: $(date)" >> $OUTPUT_FILE
echo "curr1_input: $CURR1" >> $OUTPUT_FILE
echo "in1_input: $IN1" >> $OUTPUT_FILE
echo "=========================" >> $OUTPUT_FILE

# Inform the user
echo "Readings saved to $OUTPUT_FILE"

