import subprocess
import sys
import os
import re

ManagerApp_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ManagerApp'))
sys.path.append(ManagerApp_folder_path)
from manageExecution import get_current_time


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
        gpu_power_output = subprocess.check_output("sudo " + gpu_power_script, shell=True, universal_newlines=True, stderr=subprocess.STDOUT).splitlines()
        

        gpu_freq_script = "cat /sys/devices/gpu.0/devfreq/57000000.gpu/cur_freq"
        gpu_frequency = subprocess.check_output(gpu_freq_script, shell=True, universal_newlines=True, stderr=subprocess.STDOUT).strip()
        print("GPU freq: " + gpu_frequency)

        for line in gpu_power_output:
            if "Power:" in line:
                gpu_power = line.split("Power:")[1].split("W")[0].strip()  # This will get the power value
                print("GPU Power:", gpu_power, "W")
                break

        tegrastats_output = subprocess.check_output(tegrastats_script, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        
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

    

    return [float(gpu_temperature) , int(gpu_frequency), float(gpu_power) , int(ram_used), int(ram_total), int(gpu_usage)]




def update_freqFile():
    gpu_freq_script = "cat /sys/devices/gpu.0/devfreq/57000000.gpu/cur_freq"
    try:        
        # Execute the command and capture the output
        gpu_frequency = subprocess.check_output(gpu_freq_script, shell=True, universal_newlines=True, stderr=subprocess.STDOUT).strip()
        gpu_frequency= int(gpu_frequency)/1000000                    
    except subprocess.CalledProcessError as e:                                
        print("Failed to get GPU frequency:", e)
        return
    
    current_time =get_current_time()[0]
    current_time =  round( current_time, 2)
    filename = "frequency_report.txt"
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found, creating new file")
        lines = ["Time samples\n", "\n", "Frequency samples\n", "\n"]


    # Modify the lines where time and frequency samples are stored
    for i, line in enumerate(lines):
        if "Time samples" in line:
            if lines[i+1].strip():  # Check if the next line is not just a newline character
                lines[i+1] = lines[i+1].strip() + f"{current_time:.2f},\n"
            else:
                lines[i+1] = f"{current_time}\n"
        elif "Frequency samples" in line:
            if lines[i+1].strip():
                lines[i+1] = lines[i+1].strip() + f",{gpu_frequency}\n"
            else:
                lines[i+1] = f"{gpu_frequency}\n"

    # Write the modified content back to the file
    with open(filename, "w") as file:
        file.writelines(lines)
    
    create_limited_freqFile(gpu_frequency, current_time)


def create_limited_freqFile(gpu_frequency, current_time):
    filename = "limited_frequency_report.txt"
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found, creating new file")
        lines = ["Time samples\n", "\n", "Frequency samples\n", "\n"]

    # Find the indices of "Time samples" and "Frequency samples" sections
    time_samples_index = None
    freq_samples_index = None
    for i, line in enumerate(lines):
        if "Time samples" in line:
            time_samples_index = i + 1
        elif "Frequency samples" in line:
            freq_samples_index = i + 1

    # Extract time and frequency samples
    time_samples = [float(t) for t in lines[time_samples_index].strip().split(",")] if time_samples_index is not None else []
    freq_samples = [float(f) for f in lines[freq_samples_index].strip().split(",")] if freq_samples_index is not None else []

    # Append new values and limit each section to a maximum of 200 elements
    time_samples.append(current_time)
    freq_samples.append(gpu_frequency)
    time_samples = time_samples[-200:]
    freq_samples = freq_samples[-200:]

    # Update lines with modified time and frequency samples
    if time_samples_index is not None:
        lines[time_samples_index] = ",".join([f"{t:.2f}" for t in time_samples]) + "\n"
    else:
        lines.insert(time_samples_index, ",".join([f"{t:.2f}" for t in time_samples]) + "\n")
    if freq_samples_index is not None:
        lines[freq_samples_index] = ",".join([f"{f:.2f}" for f in freq_samples]) + "\n"
    else:
        lines.insert(freq_samples_index, ",".join([f"{f:.2f}" for f in freq_samples]) + "\n")

    # Write the modified content back to the file
    with open(filename, "w") as file:
        file.writelines(lines)



if __name__ == '__main__':
    monitor_gpu()

