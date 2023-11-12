import sys
import os 
# Add the path to the json_folder directory to sys.path
ManagerApp_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ManagerApp'))
Monitor_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Monitoring'))

sys.path.append(ManagerApp_folder_path)
sys.path.append(Monitor_folder_path)

from flask import Flask, jsonify, request, send_file, Response
import threading
import time
import subprocess
from flask_cors import CORS #allow the server and front-end to run on different domains( different ports are considered different domains)
from jsonParsing import transform_input_json 
from manageExecution import manageExecution, current_apps, get_current_time, time_flags
from manageMetrics import writeCSV
from monitoring import monitor_gpu


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

execution_complete = threading.Event()

gpu_iterations_data = {
    "temperature" : [],
    "power":[],
    "current_time":[],
    "iteration_time":[],
    "execution_time" : [],
    "ram_used": [],
    "gpu_usage": [],    
    "iteration_time_avg":0,
    "temp_avg" : 0,
    "power_avg" : 0,
    "ram_avg" : 0,
    "gpu_usage_avg":0
}


global_gpu_data = {
    "temperature": None,
    "frequency": None,
    "power": None,
    "ram_used":None
}


execution_data = {            
        "gpu_iterations_data": gpu_iterations_data,                        
        "global_gpu_data": global_gpu_data,                                    
        "global_current_apps": []                                         
}

def setAvgData():
    powerArray = gpu_iterations_data['power']
    if len(powerArray) != 0:
        gpu_iterations_data['power_avg'] = sum(powerArray)/len(powerArray)
        
    tempArray = gpu_iterations_data['temperature']
    if len(tempArray) != 0 :
        gpu_iterations_data['temp_avg'] = sum(tempArray)/len(tempArray)
    
    iterArray = gpu_iterations_data['iteration_time']
    if len(iterArray) != 0: 
        gpu_iterations_data['iteration_time_avg'] = sum(iterArray)/len(iterArray)
    
    ramArray = gpu_iterations_data['ram_used']
    if len(ramArray) != 0:
        gpu_iterations_data['ram_avg'] = sum(ramArray) / len(ramArray)
    
    gpu_usageArray = gpu_iterations_data['gpu_usage']
    if len(ramArray) != 0:
        gpu_iterations_data['gpu_usage_avg'] = sum(gpu_usageArray) / len(gpu_usageArray)

    print(gpu_iterations_data)


def gpu_monitor_thread():
    
    global global_gpu_data
    global gpu_iterations_data

    try:
        
        gpu_data = monitor_gpu() 
        print("monitor output:" , gpu_data) 
        global_gpu_data["temperature"] = gpu_data[0]
        gpu_iterations_data['temperature'].append(gpu_data[0])

        global_gpu_data["frequency"] = gpu_data[1]

        global_gpu_data["power"] = gpu_data[2]
        gpu_iterations_data['power'].append(gpu_data[2])

        global_gpu_data["ram_used"] = gpu_data[3]
        gpu_iterations_data['ram_used'].append(gpu_data[3])

        gpu_iterations_data['gpu_usage'].append(gpu_data[5])       
        current_time, iterations_time = get_current_time()

        if current_time != 0 :
            gpu_iterations_data["current_time"].append(current_time)

        if iterations_time !=[]:
            gpu_iterations_data['iteration_time'] = iterations_time

        print("Power Array",gpu_iterations_data['power'], "Temperature Aray", gpu_iterations_data['temperature'], "RAM", gpu_iterations_data["ram_used"])
        
    except Exception as e:
        print(f"Exception in gpu_monitor_thread: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
           



#GET METHODS


@app.route('/gpu_data', methods=['GET'])
def get_gpuData():
    start_time , end_time= time_flags()
    print("Start and END", start_time,"  ", end_time)
    if start_time is not None and end_time is None:
    
        execution_data['gpu_iterations_data'] = gpu_iterations_data
        execution_data['global_gpu_data'] = global_gpu_data

        if current_apps == []:
            execution_data['global_current_apps'] = ""
        
        else:
            execution_data['global_current_apps']= list(current_apps)    
        
        gpu_monitor_thread()
        response = jsonify(execution_data)
        response.headers['ngrok-skip-browser-warning'] = '1'
    else:
        response = jsonify("out of execution")
        response.headers['ngrok-skip-browser-warning'] = '1'
    print(response.get_json())    
    return response



@app.route('/get-csv', methods=['GET'])
def get_csv():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_file = os.path.join(current_directory, 'execution_results.csv')
    
    response = send_file(path_to_file, as_attachment=True, download_name='execution_results.csv')

    # Add your custom header here
    response.headers['ngrok-skip-browser-warning'] = '1'

    return response

@app.route('/frequencies', methods=['GET'])
def get_frequencies():
    response = jsonify(frequencies)
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response


@app.route('/bfs_workloads', methods=['GET'])
def get_BFSworkloads():
    response = jsonify(bfs_workloads)
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response

@app.route('/cfd_workloads', methods=['GET'])
def get_CFDworkloads():
    response = jsonify(cfd_workloads)
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response


#POST METHODS

# Define a route to receive POST requests and store data in executionRequest
@app.route('/setExecutionRequest', methods=['POST', 'OPTIONS'])
def execution_request():
    global executionRequest
    global global_gpu_data
    global gpu_iterations_data

    if request.method == 'OPTIONS':
               
        headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type', 
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
                                                               
                }
                
        return ('', 200, headers)

    data = request.get_json()
    executionRequest = data
    print(executionRequest)

    #Transform the input to the JSON expected format of the managerApp
    executionJson =  transform_input_json(executionRequest)
    print(executionJson)
    
    gpu_iterations_data = {
        "temperature" : [],
        "power":[],
        "iteration_time": [],
        "current_time":[],
        "iteration_time_avg": 0,
        "ram_used" : [],
        "gpu_usage": [],
        "temp_avg" : 0,
        "power_avg" : 0,
        "ram_avg" : 0,
        "gpu_usage_avg":0
    }


    global_gpu_data = {
        "temperature": None,           
        "frequency": None,
        "power": None,
        "ram_used" : None
    }
    
    appNames, workloads, exec_num, exec_type, freq, total_execTime = manageExecution(executionJson)
    
    setAvgData()
    input_filename = "execution_results.txt"    
    csv_filename = 'execution_results.csv'

    power_avg = gpu_iterations_data['power_avg']
    temp_avg = gpu_iterations_data['temp_avg']
    ram_avg = gpu_iterations_data['ram_avg']
    iterations_execTime = gpu_iterations_data['iteration_time']
    gpu_usage_avg = gpu_iterations_data['gpu_usage_avg']
    
    writeCSV(csv_filename,input_filename, appNames, exec_num, exec_type, freq, power_avg, temp_avg, 
             ram_avg, workloads, total_execTime, iterations_execTime, gpu_usage_avg)
  

    return jsonify({"message": "Execution request processed successfully."})


# Run the Flask application on a local development server
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
    
