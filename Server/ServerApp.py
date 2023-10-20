from flask import Flask, jsonify, request
import threading
import subprocess
from flask_cors import CORS #allow the server and front-end to run on different domains( different ports are considered different domains)

# Create a Flask web application
app = Flask('evaluatorServer')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # This enables JSON pretty-printing
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Sample array of app names
appsNames= {
    "itemNames" : ['bfs', 'lud']
}

workloadsNames= {
    "itemNames" : ['graph65536.txt', '256.dat']
}

# This function will run your executable.
def run_managerApp():
    subprocess.run(["../../ManagerApp/managerApp"])

# This function will run your script.
def run_monitoring():
    subprocess.run(["python", "../../ManagerApp/managerApp"])


#GET METHODS

# Define a route to return the app names as JSON
@app.route('/appsNames', methods=['GET'])
def get_app_names():
    # Convert the array to JSON
    response = jsonify(appsNames)
    # Add the 'ngrok-skip-browser-warning' header to the response
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response

# Define a route to return the workloads names as JSON
@app.route('/workloadsNames', methods=['GET'])
def get_workloads_names():
    #Convert the array to JSON
    response = jsonify(workloadsNames)

    # Add the 'ngrok-skip-browser-warning' header to the response
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response 


#POST METHODS

# Define a route to receive POST requests and store data in executionRequest
@app.route('/setExecutionRequest', methods=['POST', 'OPTIONS'])
def execution_request():

    if request.method == 'OPTIONS':
               
        headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',                                            'Access-Control-Allow-Methods': 'POST, OPTIONS'
                                                               
                }
                
        return ('', 200, headers)



    global executionRequest
    data = request.get_json()
    executionRequest = data
    print(executionRequest)
   

    #thread1 = threading.Thread(target=run_managerApp)  # This thread will run the executable
    #thread2 = threading.Thread(target=run_monitoring)      # This thread will run the script

    # Start the two threads
    #thread1.start()
    #thread2.start()

    return jsonify({"message": "Execution request processed successfully."})


# Run the Flask application on a local development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
