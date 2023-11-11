import subprocess
import sys
import os
import re

def monitor_gpu():
    gpu_temperature=None
    gpu_frequency=None
    gpu_power = None
    gpu_usage = None
    ram_used = None
    ram_total = None
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tegrastats_script = os.path.join(script_dir, "tegrastats.sh")

        gpu_power_script = os.path.join(script_dir, "gpu_power.sh")
        gpu_power_output = subprocess.check_output("sudo " + gpu_power_script, shell=True, text=True, stderr=subprocess.STDOUT).splitlines()
        

        gpu_freq_script = "cat /sys/devices/gpu.0/devfreq/17000000.gv11b/cur_freq"
        gpu_frequency = subprocess.check_output(gpu_freq_script, shell=True, text=True, stderr=subprocess.STDOUT).strip()
        print("GPU freq: " + gpu_frequency)

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
                match = re.search(r'GR3D_FREQ (\d+)%', line)
                if match:                                                    
                    gpu_usage = int(match.group(1))
                    print("GR3D_FREQ:", gpu_usage, "%")  
            if "RAM" in line:               
                ram_parts = line.split("RAM")[1].split('/')[0].strip()
                ram_used = ram_parts.split('MB')[0].strip()
                ram_total = line.split("RAM ")[1].split('/')[1].split('MB')[0].strip()
                print("RAM Used:", ram_used)
                print("RAM Total:", ram_total)
                break

    except subprocess.CalledProcessError as e:
        print("Error: ", e.output)
    
    except KeyboardInterrupt:
        print("Monitoring stopped by user. ")

    

    return [float(gpu_temperature) , int(gpu_frequency), float(gpu_power) , int(ram_used), int(ram_total)]


if __name__ == '__main__':
    monitor_gpu()

