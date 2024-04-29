# jetson-gpu-benchmarking

## Execution

### Install Ngrok

Download and install Ngrok from [here](https://ngrok.com/download).

### Install Flask

To install Flask, run the following command:

```bash
pip3 install Flask
pip3 install flask-socketio
pip3 install flask-cors


```

### Install NumPy and SciPy

Run the following command:

```bash
pip3 install numpy scipy
```

### Running the Server

Navigate to the server directory and run the server:

```bash
cd Server
sudo python3 ServerApp.py
```

### Exposing the Server Using Ngrok
To expose the server using Ngrok, run the following command, replacing 192.168.20.15:5000 with the address and port of your server:

```bash
ngrok http 192.168.20.13:5000
```
This will provide you with a public URL that you can use to access your Flask server from anywhere on the internet.

### Configuring the React Application
In your React application, adjust the ngrokURL in **./WebApp/gpu-metric-framework/src/App.js** to match the public URL provided by Ngrok:

```bash
const ngrokURL = "https://3109-141-3-72-67.ngrok-free.app/";
```
