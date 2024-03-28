#!/bin/bash

# Start Ngrok in the background
ngrok http 192.168.20.15:5000 &

# Give Ngrok some time to establish the tunnel
sleep 2

# Retrieve the public URL from Ngrok's API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Print the URL
echo "Ngrok URL: $NGROK_URL"

# You can now use $NGROK_URL in your application

