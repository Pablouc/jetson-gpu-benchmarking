

GPU_temp=$(cat /sys/class/thermal/thermal_zone2/temp)

gpu=$((GPU_temp/1000))

echo "GPU $gpu°C"

