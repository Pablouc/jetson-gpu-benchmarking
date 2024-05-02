import sys
import os 
# Add the path to the json_folder directory to sys.path
ManagerApp_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ManagerApp'))
Monitor_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Monitoring'))

sys.path.append(ManagerApp_folder_path)
sys.path.append(Monitor_folder_path)

from flask import Flask, jsonify, request, send_file, Response
from flask_socketio import SocketIO, emit
import threading
from threading import Thread
import uuid
import time
from zipfile import ZipFile
import subprocess
from flask_cors import CORS #allow the server and front-end to run on different domains( different ports are considered different domains)
from jsonParsing import transform_input_json 
from manageExecution import manageExecution, current_apps, get_current_time, time_flags
from manageConsole import get_console_logs, write_print_toConsole
from manageMetrics import writeCSV
from monitoring import monitor_gpu,update_freqFile


# Create a Flask web application
app = Flask('evaluatorServer')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # This enables JSON pretty-printing
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
#socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize SocketIO with CORS allowed

frequencies = ['76800000', '153600000', '230400000', '307200000', '384000000', '460800000', '537600000', '614400000', '691200000', '768000000', '844800000', '921600000']

bfs_workloads= {
    "itemNames" : ['graph1MW_6.txt', 'graph4096.txt', 'graph65536.txt']
}

gauss_workloads= {
    "itemNames" : ['matrix1024.txt',  'matrix16.txt',  'matrix2048.txt',  'matrix208.txt']
}
injection_fault = False
stop_event = threading.Event()
FREQ_REQ_TIME = 0.001

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

    #print(gpu_iterations_data)


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

        #print("Power Array",gpu_iterations_data['power'], "Temperature Aray", gpu_iterations_data['temperature'], "RAM", gpu_iterations_data["ram_used"])
        
    except Exception as e:
        print(f"Exception in gpu_monitor_thread: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


def update_frequency_file(stop_event):
    while not stop_event.is_set():
        update_freqFile()
        time.sleep(FREQ_REQ_TIME)


def send_frequency_task(stop_event):

    file_path = './limited_frequency_report.txt'
    log_file_path = './frequency_log.txt'
        
    # Open the log file in append mode
    log_file = open(log_file_path, 'a')

    # Redirect stdout and stderr to the log file
    sys.stdout = log_file
    sys.stderr = log_file
    while not stop_event.is_set():
        try:        
            with open(file_path, 'r') as file:
                file_content = file.read()
            
            socketio.emit('file_transfer', {'file_content': file_content, 'filename': file_path})
            
            # Reverting stdout back to its original value
            #sys.stdout = sys.__stdout__
        except Exception as e:                                                
            print(f"Failed to send file: {e}")
            socketio.emit('error', {'message': 'Failed to send file', 'error': str(e)})
        time.sleep(1)
    
    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    log_file.close()

def background_task():
    last_console_length=0
    while True:
        console_logs = get_console_logs()
        if last_console_length != len(console_logs):
        
            last_console_length = len(console_logs)
            # Redirecting stdout to /dev/null to suppress print statements
            sys.stdout = open('/dev/null', 'w')
            socketio.emit('response', {'console_logs': console_logs})
            # Reverting stdout back to its original value
            sys.stdout = sys.__stdout__
        time.sleep(0.5)  
    

# Define a socket event for 'message'
@socketio.on('message')
def handle_message(data):
    try:
        print('received message: ' + data)

    except Exception as e:
        print(f"Error processing message: {e}")
        #Emit an error response
        emit('response', {'data': 'Error processing message', 'error': str(e)})


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
    return response



@app.route('/get-csv', methods=['GET'])
def get_csv():
    global injection_fault
    current_directory = os.path.dirname(os.path.abspath(__file__))

    if injection_fault == False:
        path_to_file = os.path.join(current_directory, 'execution_results.csv')
        response = send_file(path_to_file, as_attachment=True, download_name='execution_results.csv')
        response.headers['ngrok-skip-browser-warning'] = '1'
        return response

    else:
        file1 = os.path.join(current_directory, 'execution_results.csv')
        file2 = os.path.join(current_directory, '../benchmarks/gpu-rodinia/cuda/gaussian/originalSol2048.txt')
        file3 = os.path.join(current_directory, '../benchmarks/gpu-rodinia/cuda/gaussian/solutionVector.txt')
        zip_filename = os.path.join(current_directory, 'execution_results.zip')

        with ZipFile(zip_filename, 'w') as zipf:
            zipf.write(file1, arcname=os.path.basename(file1))
            zipf.write(file2, arcname=os.path.basename(file2))
            zipf.write(file3, arcname=os.path.basename(file3))
            zipf.close()

        response = send_file(zip_filename, mimetype='application/zip', as_attachment=True,download_name='execution_results.zip')
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

@app.route('/gauss_workloads', methods=['GET'])
def get_GAUSSworkloads():
    response = jsonify(gauss_workloads)
    response.headers['ngrok-skip-browser-warning'] = '1'
    
    return response


#POST METHODS

# Define a route to receive POST requests and store data in executionRequest
@app.route('/setExecutionRequest', methods=['POST', 'OPTIONS'])
def execution_request():
    global executionRequest

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
    task_id = background_execution(executionRequest)
    return jsonify({"message": "Execution started", "task_id": task_id})


def background_execution(executionRequest):
    

    def task():
        result = executionTask(executionRequest)
        socketio.emit('task_complete', {'task_id': thread.name, 'result': result})
    
    thread = threading.Thread(target=task, name=f"task-{uuid.uuid4()}")
    thread.start()
    return thread.name



def executionTask(executionRequest):
    global global_gpu_data
    global gpu_iterations_data
    global injection_fault
    global stop_event
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
    frequency_report_path= './frequency_report.txt'
    if os.path.exists(frequency_report_path):
        os.remove(frequency_report_path)
    
    injection_fault = False

    stop_event = threading.Event()
    thread_updateFreq = threading.Thread(target=update_frequency_file, args=(stop_event,))
    thread_sendFreq = Thread(target=send_frequency_task, args=(stop_event,))
    thread_updateFreq.start()
    thread_sendFreq.start()
    appNames, workloads, exec_num, exec_type, freq, total_execTime, execution_result = manageExecution(executionJson)
    
    stop_event.set()
    thread_updateFreq.join()
    thread_sendFreq.join()

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
    
    if execution_result == 0:
        return jsonify({"message": "Execution request processed successfully."})
    else:
        injection_fault = True
        return jsonify({"message": "Execution stoped due to injection fault"})


# Run the Flask application on a local development server
if __name__ == '__main__':
    
    thread = Thread(target=background_task)
    thread.start()
    
    #app.run(threaded=True, host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000)
    
