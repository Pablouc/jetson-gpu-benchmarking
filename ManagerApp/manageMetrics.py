import os
import re

script_directory = os.path.dirname(os.path.abspath(__file__))

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

# Example usage:
if __name__ == "__main__":
    filename = "execution_results.txt"  # Replace with the path to your text file

    lud = Lud(filename)
    print("LUD")
    print("Time Consumed Values:", lud.time_consumed , '\n')

    particle = Particle(filename)
    print('Particle Filter')
    print("VIDEO SEQUENCE TOOK:", particle.video_sequence)
    print("TIME TO SEND TO GPU:", particle.timeToSend_to_gpu)
    print("GPU Execution:", particle.gpu_execution)
    print("FREE TIME:", particle.free_time)
    print("PARTICLE FILTER TOOK:", particle.particle_filter)
    print("ENTIRE PROGRAM TOOK:", particle.entire_program , '\n')

    cfd = Cfd(filename)
    print('CFD')
    print("Seconds per Iteration:", cfd.seconds_per_iteration, '\n')

    lava_md = LavaMD(filename)
    print('LavaMD')
    print("SET DEVICE:", lava_md.set_device)
    print("MEM COPY IN:", lava_md.mem_copy_in)
    print("KERNEL:", lava_md.kernel)
    print("MEM COPY OUT:", lava_md.mem_copy_out)
    print("MEM FREE:", lava_md.mem_free)
    print("TOTAL:", lava_md.total, '\n')

    bfs = BFS(filename)
    print('BFS')
    print("HtoD:", bfs.host_to_dev)
    print("DtoH:", bfs.dev_to_host)
    print("Exec:", bfs.execution)
    print("Total:", bfs.total, '\n')

    srad = Srad(filename)
    print('Srad')
    print("RESIZE IMAGE:", srad.resize_image)
    print("COPY DATA TO CPU->GPU:", srad.host_to_dev)
    print("EXTRACT IMAGE:", srad.extract_image)
    print("COMPRESS IMAGE:", srad.compress_image)
    print("COMPUTE:", srad.compute)
    print("COPY DATA TO GPU->CPU:", srad.dev_to_host)
    print("GPU DRIVER INIT, CPU/GPU SETUP, MEMORY ALLOCATION:", srad.gpu_cpu_mem_setup)
    print("TOTAL:", srad.total, '\n ')