import os
import subprocess
import time
import threading
import sys

WickedApp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'WickedApp'))
sys.path.append(WickedApp_path)

from wickedApp import result_validation
from manageConsole import get_console_logs, write_console_log, write_print_toConsole, reset_console

# Define a global variable to store the total execution time
total_execution_time = 0
iterations_timeStats=[]
executing = False
start_time= None
end_time = None
current_apps = set()


# Create a lock to ensure that only one thread updates the total_execution_time at a time
lock = threading.Lock()
    
class App:
    def __init__(self, name, workloads, threads, external, make_flag, make_input):
        self.name = name
        self.workloads = workloads
        self.threads = threads
        self.external = external
        self.make_flag = make_flag
        self.make_input = make_input


def get_current_time():
    global start_time
    global iterations_timeStats
    
    if start_time != None:
        current_time = time.time() - start_time
    else:
        current_time = 0
    return [current_time, iterations_timeStats]


def time_flags():
    global start_time, end_time

    return [start_time, end_time]

def process_input(data):
    apps_list = []

    for app_data in data['apps']:
        name = app_data['name']
        workloads = app_data['workloads']
        threads = ''

        # Check if the app is "Lud" or "CFD" to include threads
        if name in ["Lud", "CFD"]:
            threads = app_data.get('threads', '')

        app_instance = App(name, workloads, threads, False, False,'')
        
        if name == "Wicked":
            apps_list.insert(0, app_instance)  # Insert "Wicked" at the first position
        else:
            apps_list.append(app_instance)

    return apps_list, data['execType'], data['execNum'], data['freq']

def process_externalApp(data):
    apps_list = []

    for app_data in data['external_app']:
        name = app_data['appName']
        workloads = app_data['workload_input']
        threads = ''
        make_flag = app_data['makefile_flag']
        make_input = app_data['makefile_input']
        app_instance = App(name, workloads, threads, True, make_flag, make_input)
        apps_list.append(app_instance)

    return apps_list

def customize_makefile(command):
    command_res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(command)
    if command_res.returncode == 0 :
        write_console_log(command_result,'stdout')
        print("Makefile executed succesfully")
        print(command_res.stdout)

    else:
        write_console_log(command_result,'stderr')
        print("Error executing the makefile")
        print(command_res.stderr)


def run_script(path, appName):
    global console_output
    command_result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if command_result.returncode == 0:
        print("Command executed successfully.")
        print( appName +" Output:")
        print(command_result.stdout)
        write_console_log(command_result,'stdout')
        
        # Append the output to the specified file       
        with open('execution_results.txt', 'a') as file:                    
            file.write(command_result.stdout)
            file.write('\n')  
            file.write('\n')
            file.write('\n')# Add a newline to separate multiple runs

    else:
        write_console_log(command_result,'stderr')
        print(f"Error executing the command. Exit code: {command_result.returncode}")
        print( appName + " Error output:")
        print(command_result.stderr)


def run_script_repeatedly(script, delay):
    while True:
        run_script(script)
        time.sleep(delay)


def run_application(script, appName, simultFlag):
    global current_app

    # Start of application execution; add to the current_apps set
    with lock:
        current_apps.add(appName)

    # If simultFlag is 0, acquire the lock to ensure sequential execution
    if simultFlag == 0:
        with lock:           
            pass
        run_script(script, appName)              
    else:
                              
        run_script(script, appName)

    # End of application execution; remove from the current_apps set
    
    with lock:
        current_apps.remove(appName)

        

def create_makefiles(apps):
    benchmark_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'benchmarks'))
    appsPath = benchmark_path + "/gpu-rodinia/bin/linux/cuda/"
    for app in apps:
        if app.name == "Lud":
            make_path = benchmark_path + "/gpu-rodinia/cuda/lud/cuda/"
            customize_makefile(f"cd {make_path} && make clean")
            customize_makefile(f"export PATH=/usr/local/cuda/bin:$PATH && cd {make_path} && make RD_WG_SIZE={app.threads}")
            customize_makefile(f"cd {make_path} && cp lud_cuda {appsPath}")
            

        elif app.name == "CFD":
            make_path = benchmark_path + "/gpu-rodinia/cuda/cfd/"
            customize_makefile(f"cd {make_path} && make clean") 
            customize_makefile(f"export PATH=/usr/local/cuda/bin:$PATH && cd {make_path} && make RD_WG_SIZE={app.threads}")
            customize_makefile(f"cd {make_path} && cp euler3d {appsPath}")



def simultExecution(apps, iterations, frequency):
    global executing
    global start_time, end_time
    global iterations_timeStats

    #Scaling the frequency
    frequencyScript = 'sudo ../WickedApp/set_freq.sh ' + frequency     
    run_script(frequencyScript, "Frequency Script")
    print(frequencyScript)

    #Clearing the output file 
    with open('execution_results.txt',"w") as file:
        pass
    
    #Defining Paths  
    appsPath ='sudo ../benchmarks/gpu-rodinia/bin/linux/cuda/'
    wickedApp_Path= 'sudo ../WickedApp/freq_scalator.sh'
    workloadsPath = '../benchmarks/gpu-rodinia/data/'
    output_Path = '../benchmarks/gpu-rodinia/cuda/'
    externalAppPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'benchmarks')) 

    create_makefiles(apps)

    
    #Executing Applications
    for i in range( int(iterations) ):
        threads = {}
        tempPath = ''
        appNames=[]
        wicked_running=False
        for app in apps:
            #Filling app names list for injection fault validation
            appNames.append(app.name)
            if app.name == "Wicked" and wicked_running==False:
                tempPath = wickedApp_Path + app.workloads
                wicked_running=True
            
            elif app.name == "BFS":
                tempPath = appsPath + 'bfs.out ' + workloadsPath + 'bfs/' + app.workloads 

            elif app.name == "LavaMD":
                tempPath =  appsPath + 'lavaMD ' +  app.workloads  
        
            elif app.name == "Srad":
                tempPath = appsPath + 'srad_v1 ' +  app.workloads
               
            elif app.name == "Lud":
                tempPath = appsPath + 'lud_cuda '  + app.workloads  

            elif app.name == "Gauss":
                tempPath ="sudo " + appsPath + 'gaussian -f ' + workloadsPath + 'gaussian/' + app.workloads 
                print(tempPath)
            elif app.external == True:
                tempPath = f"{externalAppPath}/{app.name}/{app.name} {app.workloads}"

            else:
                print("No app selected")
            
            if tempPath:
                thread = threading.Thread(target=run_application, args=(tempPath,app.name, 100))
                threads[app.name]= thread
                thread.start()
        
        start_time_loop = time.time()
        if i == 0:
            start_time = start_time_loop

        # Wait for all threads to finish
        for name, t in threads.items():
            if name != "Wicked":
                t.join()
        #kill Wicked App process and thread
        #run_script("sudo killall -9 freq_scalator.sh", "Wicked")
        #for name, t in threads.items():
        #    t.join()

        end_time_loop = time.time()
        if i == int(iterations) -1:
            run_script("sudo killall -9 freq_scalator.sh", "Wicked")
            #Get end time of the loop
            end_time = end_time_loop
        iteration_execTime = end_time_loop - start_time_loop
        iterations_timeStats.append(iteration_execTime)
        print("Simultaneous iteration time: ", iterations_timeStats[i]) 

        #Verify if injection fault was effective
        validation = result_validation(appNames)
        if validation == 1:
            run_script("sudo killall -9 freq_scalator.sh", "Wicked")
            end_time = end_time_loop
            print("Execution stoped due to injection fault")
            return 1
    
    return 0
    
    




def sequentialExecution(apps, iterations, frequency):
    global executing
    global start_time
    global end_time
    global iterations_timeStats


    appNames = []
    #Scaling the frequency
    executing = True
    frequencyScript = 'sudo ../WickedApp/set_freq.sh ' + frequency
    run_script(frequencyScript, "Frequency script")
    #script_thread = threading.Thread(target=run_script_repeatedly, args=(frequencyScript, 0.5))
    #script_thread.daemon = True  # Set the thread as a daemon so it exits when the main thread exits
    #script_thread.start()

    #Clearing the output file 
    with open('execution_results.txt',"w") as file:
        pass
    
    #Defining Paths
    appsPath ='../benchmarks/gpu-rodinia/bin/linux/cuda/'
    workloadsPath = '../benchmarks/gpu-rodinia/data/'
    wickedApp_Path= '../WickedApp/wickedApp.py '
    output_Path = '../benchmarks/gpu-rodinia/cuda/'
    externalAppPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'benchmarks'))
    create_makefiles(apps)

    #Executing Applications
    for i in range( int(iterations) ):
        tempPath = ''
        start_time_loop = time.time()
        if i == 0:
            start_time = start_time_loop
        for app in apps:
            
            #Filling app names list for injection fault validation
            appNames.append(app.name)

            if app.name == "BFS":
                tempPath = appsPath + 'bfs.out ' + workloadsPath + 'bfs/' + app.workloads 

            elif app.name == "LavaMD":
                tempPath = appsPath + 'lavaMD ' +  app.workloads

            elif app.name == "Wicked":
                tempPath = 'python3 ' + wickedApp_Path + app.workloads

            elif app.name == "Srad":
                tempPath = appsPath + 'srad_v1 ' +  app.workloads

            elif app.name == "Lud":
                tempPath = appsPath + 'lud_cuda '  + app.workloads 

            elif app.name == "Gauss":
                tempPath =appsPath + 'gaussian -f ' + workloadsPath + 'gaussian/' + app.workloads
            
            elif app.external == True:
                tempPath = f"{externalAppPath}/{app.name}/{app.name} {app.workloads}"
                           
            else:
                print("No app selected")
        
            if tempPath:
                # Create a thread to execute the script and measure time
                thread = threading.Thread(target=run_application, args=(tempPath,app.name, 0))
                thread.start()
                # Wait for the thread to finish
                thread.join()
                
        
        end_time_loop = time.time()  # Record end time of the loop
        if i == int(iterations) -1:
            end_time = end_time_loop
        iteration_execTime = end_time_loop - start_time_loop
        iterations_timeStats.append(iteration_execTime)
        print("Execution_Time per iteration", iterations_timeStats[i])     
            
        #Verify if injection fault was effective
        validation = result_validation(appNames)
        if validation == 1:
            end_time = end_time_loop
            print("Execution stoped due to injection fault")
            return 1
    return 0


jsonStruct = {
    'apps': [
       # {
       #     'name': 'BFS',
       #     'workloads': 'graph65536.txt'
       # },
       # {                        
       #     'name': 'LavaMD',         
       #     'workloads': '-boxes1d 10'           
       # },
        {                     
            'name': 'Wicked',
            'workloads': ' 76800000 921600000 0.05'
                           
        },
       # {
       #     'name': 'Srad',
       #     'workloads': '100 0.5 502 458'                           
       # },
        {
            'name': 'Gauss',
            'workloads': 'matrix2048.txt'
       # },
       # {
       #     'name': 'Luda',
       #     'workloads': '-s 256',
       #     'threads': '24'
        }
    ],
    'external_app': [
        {
            'appName':'pathfinder',
            'workload_input':'100000 100 20',
            'makefile_flag':'False',
            'makefile_input':'',

        }
    ],
    'execType': 'simult',
    'execNum': '2',
    'freq': '921600000'
}

def manageExternalApp(jsonStruct):
    
    appList = process_externalApp(jsonStruct)
    make_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'benchmarks'))
    for app in appList:
        if app.make_flag == True:
            if app.make_input != '':
                customize_makefile(f"cd {make_path + '/' + app.name} && make clean")
                customize_makefile(f"export PATH=/usr/local/cuda/bin:$PATH && cd {make_path + '/' + app.name} && make {app.make_input}")
    
    return appList


def manageExecution(jsonObject):
    reset_console()
    write_print_toConsole(str(jsonObject))
    #Record console outputs
    command= subprocess.run('script -a console_output.txt &&', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print("command output*********************" + command.stdout)
    global end_time, start_time, iterations_timeStats, total_execution_time,console_output
   
    execution_result=0
    apps, exec_type, exec_num, freq = process_input(jsonObject)

    if jsonObject['external_app']:
        external_apps = manageExternalApp(jsonObject)
        apps = apps + external_apps

    if exec_type == 'simult':
        execution_result = simultExecution(apps, exec_num, freq)
    
    elif exec_type == 'not-simult':
        
        execution_result = sequentialExecution(apps, exec_num, freq)
    

    #Data to be included in the csv file
    appNames =[]
    workloads =[]
    for app in apps:
        appNames.append(app.name)
        if app.threads != '':
            workloads.append(app.workloads + ' threads: ' + app.threads)
        if app.make_input != '':
            workloads.append(app.workloads + ' make_input: ' + app.make_input)
        else:
             workloads.append(app.workloads)
    ####
    
    total_execution_time = end_time - start_time    
    start_time = None
    end_time = None
    iterations_timeStats=[]  
    
    return[appNames,workloads, exec_num, exec_type, freq, total_execution_time, execution_result] 
    

if __name__ == "__main__":
    
    manageExecution(jsonStruct)
