


# Fetch the readings from the specified paths
CURRENT_VALUE=$(cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon4/curr2_input)
VOLTAGE_VALUE=$(cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon4/in2_input)

CURRENT_A=$(echo "scale=4; $CURRENT_VALUE/1000" | bc)
VOLTAGE_V=$(echo "scale=4; $VOLTAGE_VALUE/1000" | bc)

# Calculate the power
POWER_W=$(echo "$CURRENT_A * $VOLTAGE_V" | bc)

# Print the results
echo "Channel 2 (CPU + GPU + CV combined power rail):"
echo "Current: $CURRENT_A A"
echo "Voltage: $VOLTAGE_V V"
echo "Power: $POWER_W W"

