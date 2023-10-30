import subprocess

def monitor_gpu():
    gpu_temperature=None
    gpu_frequency=None
    
    try:
        tegrastats_output = subprocess.check_output("./tegrastats.sh", shell=True, text=True, stderr=subprocess.STDOUT)
        
        lines = tegrastats_output.split('\n')

        for line in lines:
            if "GPU@" in line:          
                gpu_temperature = line.split("GPU@")[1].split('C')[0].strip()
                print(gpu_temperature)

            if "GR3D_FREQ" in line:
                gpu_frequency = line.split("GR3D_FREQ")[1].split('%')[0].strip()
                print(gpu_frequency)
    except subprocess.CalledProcessError as e:
        print("Error: ", e.output)
    
    except KeyboardInterrupt:
        print("Monitoring stopped by user. ")

    

    return [gpu_temperature,gpu_frequency]


if __name__ == '__main__':
    monitor_gpu()

