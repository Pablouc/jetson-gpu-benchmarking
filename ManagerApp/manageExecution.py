import json
import subprocess

        
class App:
    def __init__(self, name, workloads, blocks, threads):
        self.name = name
        self.workloads = workloads
        self.blocks = blocks
        self.threads = threads


def process_input(data):
    # Create App instances while iterating over the input data
    apps_list = [App(app_data['name'], app_data['workloads'], app_data['blocks'], app_data['threads']) for app_data in data['apps']]
    
    # Return the list of App instances and other values
    return apps_list, data['execType'], data['execNum'], data['freq']


def modify_makefile(command):
    command_res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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
    frequencyScript = '/home/carpab00/Desktop/Pablo/Executables/freq_scalator.sh ' + frequency     
    run_script(frequencyScript)

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
            if app.name == "Bfs":
                tempPath += appsPath + 'bfs.out ' + workloadsPath + 'bfs/' + app.workloads + ' & '
            

            elif app.name == "lavaMD":
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
                tempPath += appsPath + 'lud_cuda ' +'-i '+ workloadsPath + 'lud/' + app.workloads + ' & '
                

            elif app.name == "Cfd":
                make_path = "/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/cuda/cfd/"
                if i == 0 :
                    modify_makefile(f"cd {make_path} && make clean") 
                    modify_makefile(f"cd {make_path} && make RD_WG_SIZE={app.threads}")
                    modify_makefile(f"cd {make_path} && cp euler3d {appsPath}")
                tempPath += appsPath + 'euler3d ' + workloadsPath + 'cfd/' + app.workloads + ' & '
                           
            else:
                print("No app selected")

        run_script(tempPath) 
            

        
            



        


jsonStruct = {
    'apps': [
        {
            'name': 'Bfs',
            'workloads': 'graph65536.txt',
            'blocks': '32',
            'threads': '16'
        },
        {                        
            'name': 'lavaMD',         
            'workloads': '-boxes1d 10',                          
            'blocks': '32',                           
            'threads': '16'
                           
        },
        {                     
            'name': 'Particle Filter',
            'workloads': '-x 128 -y 128 -z 10 -np 1000',             
            'blocks': '32',                              
            'threads': '16'
                           
        },
        {
            'name': 'Srad',
            'workloads': '100 0.5 502 458',              
            'blocks': '32',                              
            'threads': '16'
                           
        },
        {
            'name': 'Cfd',
            'workloads': 'fvcorr.domn.097K',               
            'blocks': '32',                               
            'threads': '16'   
        },
        {
            'name': 'Lud',
            'workloads': '256.dat',
            'blocks': '32',
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
