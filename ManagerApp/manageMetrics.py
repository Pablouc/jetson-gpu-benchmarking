import os
import re
import csv

script_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Server'))

class Lud:
    def __init__(self, filename):
        self.time_consumed = []
        self.read_file(filename)
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    if "Time consumed(ms):" in line:
                        try:
                            value = line.split(":")[1].strip()
                            self.time_consumed.append(value)
                        except ValueError:
                            pass
                    line = file.readline()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class Gauss:
    def __init__(self, filename):
        self.clock_rate = []
        self.total_time = []
        self.kernel_time = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "Clock rate" in line:
                        self.clock_rate.append(float(line.split()[-2]))  # Assuming the value is before the last word "KHz"
                    elif "Time total" in line:
                        self.total_time.append(float(line.split()[-2]))  # Assuming the value is before the last word "sec"
                    elif "Time for CUDA kernels" in line:
                        self.kernel_time.append(float(line.split()[-2]))  # Assuming the value is before the last word "sec"
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class Particle:
    def __init__(self, filename):
        self.video_sequence = []
        self.timeToSend_to_gpu = []
        self.gpu_execution = []
        self.free_time = []
        self.particle_filter = []
        self.entire_program = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "VIDEO SEQUENCE TOOK" in line:
                        self.video_sequence.append(float(line.split()[-1]))
                    elif "TIME TO SEND TO GPU:" in line:
                        self.timeToSend_to_gpu.append(float(line.split()[-1]))
                    elif "GPU Execution:" in line:
                        self.gpu_execution.append(float(line.split()[-1]))
                    elif "FREE TIME:" in line:
                        self.free_time.append(float(line.split()[-1]))
                    elif "PARTICLE FILTER TOOK" in line:
                        self.particle_filter.append(float(line.split()[-1]))
                    elif "ENTIRE PROGRAM TOOK" in line:
                        self.entire_program.append(float(line.split()[-1]))
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class Cfd:
    def __init__(self, filename):
        self.seconds_per_iteration = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "Name:" in line:
                        continue  # Skip the line with "Name:"
                    if "seconds per iteration" in line:
                        seconds_str = line.strip().split()[0]
                        try:
                            seconds = float(seconds_str)
                            self.seconds_per_iteration.append(seconds)
                        except ValueError:
                            pass
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class LavaMD:
    def __init__(self, filename):
        self.set_device = []
        self.mem_copy_in = []
        self.kernel = []
        self.mem_copy_out = []
        self.mem_free = []
        self.total = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        previous_lines = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    previous_lines.append(line.strip())
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    if len(previous_lines) >= 3: 
                        parts = previous_lines[-3].split()
                        if len(parts) >= 2:
                            seconds_str = parts[0]
                            try:
                                seconds = float(seconds_str)
                                label = " ".join(parts[2:])  # Get the label after seconds
                                if label.startswith(":"):
                                    label = label[1:].strip()  # Remove leading colon if present
                                if "GPU: SET DEVICE / DRIVER INIT" in label:
                                    self.set_device.append(seconds)
                                elif "GPU MEM: ALO" in label:
                                    self.mem_copy_in.append(seconds)
                                elif "GPU: KERNEL" in label:
                                    self.kernel.append(seconds)
                                elif "GPU MEM: COPY OUT" in label:
                                    self.mem_copy_out.append(seconds)
                                elif "GPU MEM: FRE" in label:
                                    self.mem_free.append(seconds)
                                    total_time = line[:-1]
                                    self.total.append(total_time)

                            except ValueError:
                                pass
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class BFS:
    def __init__(self, filename):
        self.host_to_dev = []
        self.dev_to_host = []
        self.execution = []
        self.total = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    if line.startswith("HtoD:"):
                        seconds_str = line.split(":")[1].strip()
                        seconds = float(seconds_str)
                        self.host_to_dev.append(seconds)

                    elif line.startswith("DtoH:"):
                        seconds_str = line.split(":")[1].strip()
                        seconds = float(seconds_str)
                        self.dev_to_host.append(seconds)

                    elif line.startswith("Exec:"):
                        seconds_str = line.split(":")[1].strip()
                        seconds = float(seconds_str)
                        self.execution.append(seconds)

                    elif line.startswith("Total:"):
                        seconds_str = line.split(":")[1].strip()
                        seconds = float(seconds_str)
                        self.total.append(seconds)

        except FileNotFoundError:
            print(f"File '{filename}' not found.")


class Srad:
    def __init__(self, filename):
        self.resize_image = []
        self.host_to_dev = []
        self.extract_image = []
        self.compress_image = []
        self.compute = []
        self.dev_to_host = []
        self.gpu_cpu_mem_setup = []
        self.total = []
        full_path = os.path.join(script_directory, filename)
        self.read_file(full_path)
    def read_file(self, filename):
    
        previous_lines = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    previous_lines.append(line.strip())
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    if len(previous_lines) >= 3: 
                        parts = previous_lines[-3].split()
                        if len(parts) >= 2:
                            seconds_str = parts[0]
                            try:
                                seconds =  float(seconds_str)
                                label = " ".join(parts[2:])  # Get the label after seconds
                                if label.startswith(":"):
                                    label = label[1:].strip()  # Remove leading colon if present
                                if "RESIZE IMAGE" in label:
                                    self.resize_image.append(seconds)
                                elif "COPY DATA TO CPU->GPU" in label:
                                    self.host_to_dev.append(seconds)
                                elif "EXTRACT IMAGE" in label:
                                    self.extract_image.append(seconds)
                                elif "COMPRESS IMAGE" in label:
                                    self.compress_image.append(seconds)
                                elif "COMPUTE" in label:
                                    self.compute.append(seconds)
                                elif "COPY DATA TO GPU->CPU" in label:
                                    self.dev_to_host.append(seconds)
                                elif "GPU DRIVER INIT, CPU/GPU SETUP, MEMORY ALLOCATION" in label:
                                    self.gpu_cpu_mem_setup.append(seconds)
                                elif "FREE MEMORY" in label:
                                    total_time = line[:-1]
                                    self.total.append(total_time)

                            except ValueError:
                                pass
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

def writeCSV(csv_filename,filename ,apps, exec_num, exec_type, freq, power_avg , temp_avg, 
             ram_avg, workloads, total_execTime, iterations_execTime, gpu_usage_avg):
        # Define the CSV file name
        
        full_path = os.path.join(script_directory, csv_filename)
        print(f"CSV will be saved to: {full_path}")
        # Write the data to a CSV file
        with open(full_path, mode='w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)

            #Writing general data
            csvwriter.writerow(["Execution Type", exec_type])
            csvwriter.writerow(["Executions Number", exec_num] )
            csvwriter.writerow(["Frequency", str(freq) + ' MHz'])
            csvwriter.writerow(["Average Power consumed", str(power_avg) + ' W'])
            csvwriter.writerow(["Average GPU Temp", str(temp_avg) + ' °C'])
            csvwriter.writerow(["Average RAM used", str(ram_avg) + ' MB'])
            csvwriter.writerow(["Average GPU used", str(gpu_usage_avg) + ' %' ])
            csvwriter.writerow(["Total execution time", str(total_execTime) + ' s'])
            csvwriter.writerow([])
            csvwriter.writerow(["Workloads used by each application"])
            for i in range(len(apps)):
                csvwriter.writerow([apps[i], workloads[i]])

            csvwriter.writerow([])
            csvwriter.writerow(["Execution times per iteration"])
            for i in range(int(exec_num)):
                csvwriter.writerow([i+1, iterations_execTime[i]])
        
            csvwriter.writerow([])
            csvwriter.writerow(["Application-specific iteration metrics"])
            csvwriter.writerow([])

            if 'LavaMD' in apps:

                lava_md = LavaMD(filename)

                # Write headers
                headers = ["App", "SET DEVICE", "MEM COPY IN", "KERNEL", "MEM COPY OUT", "MEM FREE", "TOTAL"]
                if( len(lava_md.set_device)!= 0):
                    csvwriter.writerow(headers)

                # Write data for LavaMD
                for i in range(len(lava_md.set_device)):
                    row = ["LavaMD" if i == 0 else ""]
                    row.append(lava_md.set_device[i])
                    row.append(lava_md.mem_copy_in[i])
                    row.append(lava_md.kernel[i])
                    row.append(lava_md.mem_copy_out[i])
                    row.append(lava_md.mem_free[i])
                    row.append(float(lava_md.total[i].strip()))
                    csvwriter.writerow(row)

                # Calculate averages
                if(len(lava_md.set_device) != 0):
                
                    avg_set_device = sum(lava_md.set_device) / len(lava_md.set_device)
                    avg_mem_copy_in = sum(lava_md.mem_copy_in) / len(lava_md.mem_copy_in)
                    avg_kernel = sum(lava_md.kernel) / len(lava_md.kernel)
                    avg_mem_copy_out = sum(lava_md.mem_copy_out) / len(lava_md.mem_copy_out)
                    avg_mem_free = sum(lava_md.mem_free) / len(lava_md.mem_free)
                    avg_total = sum([float(x.strip()) for x in lava_md.total]) / len(lava_md.total)

                    # Write averages
                    csvwriter.writerow(["Average", avg_set_device, avg_mem_copy_in, avg_kernel, avg_mem_copy_out, avg_mem_free, avg_total])
                csvwriter.writerow([])

            if 'LUD' in apps:
                
                lud = Lud(filename)

                headers = ["App", "Time Consumed Values"]
                if( len(lud.time_consumed)!= 0):
                    csvwriter.writerow(headers)

                # Write data for LUD
                for i, value in enumerate(lud.time_consumed):
                    if i == 0:
                        csvwriter.writerow(["LUD", value])
                    else:
                        csvwriter.writerow(["", value])

                # Calculate average
                if (len(lud.time_consumed) !=0 ):
                    avg_time_consumed = sum([float(x.strip()) for x in lud.time_consumed]) / len(lud.time_consumed)

                    # Write average
                    csvwriter.writerow(["Average", avg_time_consumed])
                csvwriter.writerow([])


            if 'Particle Filter' in apps:
                
                particle = Particle(filename)

                headers = ["App", "VIDEO SEQUENCE TOOK", "TIME TO SEND TO GPU", "GPU Execution", "FREE TIME", "PARTICLE FILTER TOOK", "ENTIRE PROGRAM TOOK"]
                if( len(particle.video_sequence)!= 0):
                    csvwriter.writerow(headers)

                # Write data for Particle
                for i in range(len(particle.video_sequence)):
                    row = ["Particle Filter" if i == 0 else ""]
                    row.append(particle.video_sequence[i])
                    row.append(particle.timeToSend_to_gpu[i])
                    row.append(particle.gpu_execution[i])
                    row.append(particle.free_time[i])
                    row.append(particle.particle_filter[i])
                    row.append(particle.entire_program[i])
                    csvwriter.writerow(row)
                    

                # Calculate averages
                if (len(particle.entire_program) != 0 ):
                    avg_video_sequence = sum(particle.video_sequence) / len(particle.video_sequence)
                    avg_timeToSend_to_gpu = sum(particle.timeToSend_to_gpu) / len(particle.timeToSend_to_gpu)
                    avg_gpu_execution = sum(particle.gpu_execution) / len(particle.gpu_execution)
                    avg_free_time = sum(particle.free_time) / len(particle.free_time)
                    avg_particle_filter = sum(particle.particle_filter) / len(particle.particle_filter)
                    avg_entire_program = sum(particle.entire_program) / len(particle.entire_program)

                    # Write averages
                    csvwriter.writerow(["Average", avg_video_sequence, avg_timeToSend_to_gpu, avg_gpu_execution, avg_free_time, avg_particle_filter, avg_entire_program])
                csvwriter.writerow([])

            if 'CFD' in apps:

                cfd = Cfd(filename)

                headers = ["App", "Seconds per Iteration"]
                if( len(cfd.seconds_per_iteration)!= 0):
                    csvwriter.writerow(headers)

                # Write data for Cfd
                for i in range(len(cfd.seconds_per_iteration)):
                    row = ["CFD" if i == 0 else ""]
                    row.append(cfd.seconds_per_iteration[i])
                    csvwriter.writerow(row)

                if (len(cfd.seconds_per_iteration) !=0):
                    # Calculate average
                    avg_seconds_per_iteration = sum(cfd.seconds_per_iteration) / len(cfd.seconds_per_iteration)

                    # Write average
                    csvwriter.writerow(["Average", avg_seconds_per_iteration])
                
                csvwriter.writerow([])

            if 'BFS' in apps:

                bfs = BFS(filename)

                # Write headers
                headers = ["App", "HtoD", "DtoH", "Exec", "Total"]
                if( len(bfs.host_to_dev)!= 0):
                    csvwriter.writerow(headers)

                # Write data for BFS
                for i in range(len(bfs.host_to_dev)):
                    row = ["BFS" if i == 0 else ""]
                    row.append(bfs.host_to_dev[i])
                    row.append(bfs.dev_to_host[i])
                    row.append(bfs.execution[i])
                    row.append(bfs.total[i])
                    csvwriter.writerow(row)

                # Calculate averages
                if ( len(bfs.total) != 0 ):
                    avg_host_to_dev = sum(bfs.host_to_dev) / len(bfs.host_to_dev)
                    avg_dev_to_host = sum(bfs.dev_to_host) / len(bfs.dev_to_host)
                    avg_execution = sum(bfs.execution) / len(bfs.execution)
                    avg_total = sum(bfs.total) / len(bfs.total)

                    # Write averages
                    csvwriter.writerow(["Average", avg_host_to_dev, avg_dev_to_host, avg_execution, avg_total])
                csvwriter.writerow([])
            
            if 'Srad' in apps:
                
                srad = Srad(filename)

                headers = ["App", "RESIZE IMAGE", "COPY DATA TO CPU->GPU", "EXTRACT IMAGE", "COMPRESS IMAGE", 
                   "COMPUTE", "COPY DATA TO GPU->CPU", "GPU DRIVER INIT, CPU/GPU SETUP, MEMORY ALLOCATION", "TOTAL"]
                if( len(srad.resize_image)!= 0):
                    csvwriter.writerow(headers)

                # Write data for Srad
                for i in range(len(srad.resize_image)):
                    row = ["Srad" if i == 0 else ""]
                    row.extend([
                        srad.resize_image[i], srad.host_to_dev[i], srad.extract_image[i], 
                        srad.compress_image[i], srad.compute[i], srad.dev_to_host[i], 
                        srad.gpu_cpu_mem_setup[i], srad.total[i]
                    ])
                    csvwriter.writerow(row)

                # Calculate averages
                attributes = [srad.resize_image, srad.host_to_dev, srad.extract_image, srad.compress_image, 
                            srad.compute, srad.dev_to_host, srad.gpu_cpu_mem_setup, srad.total]
                averages = ["Average"]
                for attribute in attributes:
                    if(len(srad.resize_image)!=0):
                        averages.append(sum([float(x) for x in attribute]) / len(attribute))
                
                if (len(srad.resize_image)!=0 ):
                    # Write averages
                    csvwriter.writerow(averages)
                csvwriter.writerow([])


# Example usage:
if __name__ == "__main__":
    input_filename = "execution_results.txt"  # Replace with the path to your text file

    apps = ['LUD','CFD', 'Particle Filter', 'LavaMD', 'BFS', 'Srad']
    csv_filename = 'execution_results.csv'
    writeCSV(csv_filename,input_filename, apps, 2, 'simult', 1233333, 6 , 42)
    
