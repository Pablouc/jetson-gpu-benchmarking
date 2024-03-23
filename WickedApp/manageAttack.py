import sys
import os 
import subprocess
import threading
import wickedApp

threads = []


def executeApps():
    benchmark_command = 'sudo ../benchmarks/gpu-rodinia/cuda/gaussian/gaussian -f ../benchmarks/gpu-rodinia/data/gaussian/matrix2048.txt'
    wicked_command = 'sudo python3 wickedApp.py'
    #matrixMult_command= 'sudo ./test'
    benchmark_output = '../benchmarks/gpu-rodinia/cuda/gaussian/gaussian'

    run_attack = subprocess.run(f'{benchmark_command} > {benchmark_output} & {wicked_command}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if run_attack.returncode != 0 :
        print(run_attack.stderr)


def result_validation():
    gaussian_sol = 'sudo md5sum ../benchmarks/gpu-rodinia/cuda/gaussian/originalSol2048.txt'
    gaussian_result = 'sudo md5sum ../benchmarks/gpu-rodinia/cuda/gaussian/solutionVector.txt' 

    solution_checksum_proc = subprocess.run(gaussian_sol, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    result_checksum_proc = subprocess.run(gaussian_result, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Extracting only the MD5 hash values from the command outputs
    solution_checksum = solution_checksum_proc.stdout.split()[0]
    result_checksum = result_checksum_proc.stdout.split()[0]

    print('Solution checksum' + str(solution_checksum))
    print('Result checksum: ' + str(result_checksum))

    if solution_checksum == result_checksum :
        print('Good execution')
        return 0
    else:
        print('Successful Injection Fault Attack')
        return 1



for i in range(10):
    executeApps()
    validation = result_validation()
    if validation == 1:
        break
    # thread = threading.Thread(target=executeApps, args=())
   # threads.append(thread)
   # thread.start()


#for t in threads:
   # t.join()
