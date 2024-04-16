import sys
import subprocess
import time
import os

ManagerApp_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ManagerApp'))
sys.path.append(ManagerApp_folder_path)

from manageConsole import write_console_log, write_print_toConsole

def generate_clockGlitch(iterations, min_frequency, max_frequency, delay):

    # Iterate over the range of parameters
    for i in range(0, iterations, 1):
        freqscript_command = 'sudo ../WickedApp/freq_scalator.sh '

        if i%2==0:
            freqscript_command += str(min_frequency)
        else:
            freqscript_command += str(max_frequency)

    

        # Execute the shell script with the current frequency as a parameter
        command_result = subprocess.run(freqscript_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
        if command_result.returncode != 0:
        
            print("Error executing the command. Exit code: {}".format(command_result.returncode))
            print("Error output:")
            print(command_result.stderr)
    
        
        time.sleep(delay)


def result_validation(appNames):
    make_validation = False

    for appName in appNames:
        if appName == 'Gauss':
            sol_md5_command = 'sudo md5sum ../benchmarks/gpu-rodinia/cuda/gaussian/originalSol2048.txt'
            #result_md5_command = 'sudo md5sum ../benchmarks/gpu-rodinia/cuda/gaussian/solutionVector.txt' 
            result_md5_command = 'sudo md5sum ../benchmarks/gpu-rodinia/cuda/gaussian/gaussian.cu'
            make_validation = True
        
        if make_validation == True:
            solution_checksum_proc = subprocess.run(sol_md5_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    
            result_checksum_proc = subprocess.run(result_md5_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            write_console_log(solution_checksum_proc, 'stdout')
            write_console_log(result_checksum_proc, 'stdout')
            
            # Extracting only the MD5 hash values from the command outputs
            solution_checksum = solution_checksum_proc.stdout.split()[0]
            result_checksum = result_checksum_proc.stdout.split()[0]

            print('Solution checksum of: '+ sol_md5_command+'   ' + str(solution_checksum))
         
            print('Result checksum of: ' + result_md5_command + '   ' + str(result_checksum))
            
            make_validation = False
            validation_msg=''
            if solution_checksum == result_checksum :
                validation_msg = 'Validation of attack: No Fault detected'
                write_print_toConsole(validation_msg)
                print(validation_msg)
                return 0
            else:
                validation_msg = 'Validation of attack: Successful Injection Fault Attack'
                write_print_toConsole(validation_msg)
                print(validation_msg)
                return 1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Correct usage: wickedApp.py iterations min_freq max_freq delay")
        sys.exit(1)
    generate_clockGlitch( int(sys.argv[1]) , sys.argv[2], sys.argv[3], float(sys.argv[4]))

