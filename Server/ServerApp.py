import sys
import os

# Add the path to the json_folder directory to sys.path
json_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ManagerApp'))
sys.path.append(json_folder_path)


from flask import Flask, jsonify, request, send_file
import threading
import subprocess
from flask_cors import CORS #allow the server and front-end to run on different domains( different ports are considered different domains)
from jsonParsing import transform_input_json 
from manageExecution import manageExecution

# Create a Flask web application
app = Flask('evaluatorServer')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # This enables JSON pretty-printing
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

frequencies = ['114750000', '204000000', '306000000', '408000000', '510000000', '599250000', '701250000', '752250000', '803250000',
                '854250000', '905250000', '956250000', '1007250000', '1058250000', '1109250000']

bfs_workloads= {
    "itemNames" : ['graph1MW_6.txt', 'graph4096.txt', 'graph65536.txt']
}

cfd_workloads= {
    "itemNames" : ['fvcorr.domn.097K', 'fvcorr.domn.193K', 'missile.domn.0.2M']
}

# This function will run your executable.
def run_managerApp():
    subprocess.run(["../../ManagerApp/managerApp"])

# This function will run your script.
def run_monitoring():
    subprocess.run(["python", "../../ManagerApp/managerApp"])


#GET METHODS

@app.route('/get-csv', methods=['GET'])
def get_csv():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_file = os.path.join(json_folder_path, 'execution_results.csv')
    
    response = send_file(path_to_file, as_attachment=True, download_name='execution_results.csv')

    # Add your custom header here
    response.headers['ngrok-skip-browser-warning'] = '1'

    return response

# Define a route to return the app names as JSON
@app.route('/frequencies', methods=['GET'])
def get_frequencies():
    # Convert the array to JSON
    response = jsonify(frequencies)
    # Add the 'ngrok-skip-browser-warning' header to the response
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response


# Define a route to return the app names as JSON
@app.route('/bfs_workloads', methods=['GET'])
def get_BFSworkloads():
    # Convert the array to JSON
    response = jsonify(bfs_workloads)
    # Add the 'ngrok-skip-browser-warning' header to the response
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response

# Define a route to return the app names as JSON
@app.route('/cfd_workloads', methods=['GET'])
def get_CFDworkloads():
    # Convert the array to JSON
    response = jsonify(cfd_workloads)
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
                'Access-Control-Allow-Headers': 'Content-Type', 
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
                                                               
                }
                
        return ('', 200, headers)



    global executionRequest
    data = request.get_json()
    executionRequest = data
    print(executionRequest)

    #Transform the input to the JSON expected format of the managerApp
    executionJson =  transform_input_json(executionRequest)
    print(executionJson)

    #Executing apps
    manageExecution(executionJson)
   

    #thread1 = threading.Thread(target=run_managerApp)  # This thread will run the executable
    #thread2 = threading.Thread(target=run_monitoring)      # This thread will run the script

    # Start the two threads
    #thread1.start()
    #thread2.start()

    return jsonify({"message": "Execution request processed successfully."})


# Run the Flask application on a local development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
