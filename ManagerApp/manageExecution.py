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



# This function will run your executable.
def run_script(path):
    subprocess.run([path])


def simultExecution(apps, iterations, frequency):
    
    #Scaling the frequency
    frequencyScript = './home/carpab00/Desktop/Pablo/Executables/freq_scalator.sh ' + frequency     
    run_script(frequencyScript)
    
    #Defining Paths
    appsPath ='./home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/bin/linux/cuda'   
    workloadsPath = '/home/carpab00/Desktop/Pablo/jetson-gpu-benchmarking/benchmarks/gpu-rodinia/data/'


    #Executing Applications
    for i in range( int(iterations)-1 ):
        for app in apps:
            if apps.name == "Bfs":
                tempPath = appsPath + 'bfs.out ' + workloadsPath + 'bfs/' + app.workloads
                run_script(tempPath)
            
            elif apps.name == "lavaMD":
                tempPath = appsPath + 'lavaMD ' +  app.workloads
                run_script(tempPath)
            
            elif apps.name == "Particle Filter ":
                tempPath = appsPath + 'particlefilter_float ' + app.workloads
                run_script(tempPath)

            elif apps.name == "Srad":
                tempPath = appsPath + 'srad_v1 ' +  app.workloads
                run_script(tempPath)

            elif apps.name == "Lud":
                tempPath = appsPath + 'lud_cuda ' + workloadsPath + 'lud/' + app.workloads
                run_script(tempPath)

            elif apps.name == "Cfd":
                tempPath = appsPath + 'euler3d ' + workloadsPath + 'cfd/' + app.workloads
                run_script(tempPath)
            
            else:
                print("No app selected")


            

        
            



        


jsonStruct = {
    'apps': [
        {
            'name': 'Bfs',
            'workloads': '256.dat',
            'blocks': '32',
            'threads': '16'
        },
        {
            'name': 'Lud',
            'workloads': 'graph65536.txt',
            'blocks': '32',
            'threads': '16'
        }
    ],
    'execType': 'not-simult',
    'execNum': '3',
    'freq': '1007250000'
}



apps, exec_type, exec_num, freq = process_input(jsonStruct)

# Now, you can work with the list of App instances and the other values as needed
for app in apps:
    print(app.name, app.workloads, app.blocks, app.threads)

simultExecution(apps, exec_num, freq)


