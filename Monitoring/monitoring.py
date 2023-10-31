import subprocess
import sys
import os

def monitor_gpu():
    gpu_temperature=None
    gpu_frequency=None
    gpu_power = None
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tegrastats_script = os.path.join(script_dir, "tegrastats.sh")

        gpu_power_script = os.path.join(script_dir, "gpu_power.sh")
        gpu_power_output = subprocess.check_output(gpu_power_script, shell=True, text=True, stderr=subprocess.STDOUT).splitlines()
        
        for line in gpu_power_output:
            if "Power:" in line:
                gpu_power = line.split("Power:")[1].split("W")[0].strip()  # This will get the power value
                print("GPU Power:", gpu_power, "W")
                break

        tegrastats_output = subprocess.check_output(tegrastats_script, shell=True, text=True, stderr=subprocess.STDOUT)
        
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

    

    return [gpu_temperature,gpu_frequency, gpu_power]


if __name__ == '__main__':
    monitor_gpu()

