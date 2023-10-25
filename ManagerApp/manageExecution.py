import json
import subprocess

        
class App:
    def __init__(self, name, workloads, threads):
        self.name = name
        self.workloads = workloads
        self.threads = threads


def process_input(data):
   # Create App instances while iterating over the input data
    apps_list = []

    for app_data in data['apps']:
        name = app_data['name']
        workloads = app_data['workloads']
        threads = ''

        # Check if the app is "Lud" or "CFD" to include threads
        if name in ["Lud", "CFD"]:
            threads = app_data.get('threads', '')
            print("Evaluating threads")
            print(app_data.get('threads', ''))
            print('threads: ' + threads  + '/n')


        app_instance = App(name, workloads, threads)
        apps_list.append(app_instance)
        print(app_instance.name)
        print(app_instance.workloads)
        print(app_instance.threads)

    # Return the list of App instances and other values
    return apps_list, data['execType'], data['execNum'], data['freq']


def modify_makefile(command):
    command_res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(command)
    if command_res.returncode == 0 :
        print("Makefile executed succesfully")
        print(command_res.stdout)

    else:
        print("Error executing the makefile")
        print(command_res.stderr)


# This function will run your executable.
def run_script(path):
    command_result = subprocess.run(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if command_result.returncode == 0:
        print("Command executed successfully.")
        print("Output:")
        print(command_result.stdout)

        # Append the output to the specified file       
        with open('execution_results.txt', 'a') as file:                    
            file.write(command_result.stdout)
            file.write('\n')  # Add a newline to separate multiple runs

    else:
        print(f"Error executing the command. Exit code: {command_result.returncode}")
        print("Error output:")
        print(command_result.stderr)



def simultExecution(apps, iterations, frequency):
    
    #Scaling the frequency
    frequencyScript = 'sudo /home/carpab00/Desktop/Pablo/Executables/freq_scalator.sh ' + frequency     
    run_script(frequencyScript)
    print(frequencyScript)

    #Clearing the output file 
    with open('execution_results.txt',"w") as file:
        pass
    
    #Defining Paths
    appsPath ='/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/bin/linux/cuda/'   
    workloadsPath = '/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/data/'


    #Executing Applications
    for i in range( int(iterations) ):
        tempPath = ''
        for app in apps:
            if app.name == "BFS":
                tempPath += appsPath + 'bfs.out ' + workloadsPath + 'bfs/' + app.workloads + ' & '
            

            elif app.name == "LavaMD":
                tempPath += appsPath + 'lavaMD ' +  app.workloads + ' & '
             

            elif app.name == "Particle Filter":
                tempPath += appsPath + 'particlefilter_float ' + app.workloads + ' & '
              

            elif app.name == "Srad":
                tempPath += appsPath + 'srad_v1 ' +  app.workloads + ' & '
               

            elif app.name == "Lud":
                make_path = "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/lud/cuda/"
                
                if i == 0 :
                    modify_makefile(f"cd {make_path} && make clean")
                    modify_makefile(f"cd {make_path} && make RD_WG_SIZE={app.threads}")
                    modify_makefile(f"cd {make_path} && cp lud_cuda {appsPath}")
                tempPath += appsPath + 'lud_cuda '  + app.workloads + ' & '
                

            elif app.name == "CFD":
                make_path = "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/cfd/"
                if i == 0 :
                    modify_makefile(f"cd {make_path} && make clean") 
                    modify_makefile(f"cd {make_path} && make RD_WG_SIZE={app.threads}")
                    modify_makefile(f"cd {make_path} && cp euler3d {appsPath}")
                tempPath += appsPath + 'euler3d ' + workloadsPath + 'cfd/' + app.workloads + ' & '
                           
            else:
                print("No app selected")
        
        print(tempPath)
        run_script(tempPath) 
            

        
            



        


jsonStruct = {
    'apps': [
        {
            'name': 'BFS',
            'workloads': 'graph65536.txt'
        },
        {                        
            'name': 'LavaMD',         
            'workloads': '-boxes1d 10'           
        },
        {                     
            'name': 'Particle Filter',
            'workloads': '-x 128 -y 128 -z 10 -np 1000'
                           
        },
        {
            'name': 'Srad',
            'workloads': '100 0.5 502 458'                           
        },
        {
            'name': 'CFD',
            'workloads': 'fvcorr.domn.097K',               
            'threads': '16'   
        },
        {
            'name': 'Lud',
            'workloads': '-s 256',
            'threads': '24'
        }
    ],
    'execType': 'simult',
    'execNum': '3',
    'freq': '1007250000'
}


def manageExecution(jsonObject):
    
    apps, exec_type, exec_num, freq = process_input(jsonObject)

    if exec_type == 'simult':
        simultExecution(apps, exec_num, freq)


manageExecution(jsonStruct)
