import matplotlib
matplotlib.use('Agg')

import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt


# Path to the file
file_path = "../Server/frequency_report.txt"


def read_and_process_file(file_path):
    time_samples = []
    frequency_samples = []
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        time_index = next(i for i, line in enumerate(lines) if line.startswith("Time samples"))
        frequency_index = next(i for i, line in enumerate(lines) if line.startswith("Frequency samples"))

        if time_index + 1 < len(lines):
            raw_time_data = lines[time_index + 1].strip().split(',')
            #filtered_time_data = [float(num) for num in raw_time_data if num.strip()]
            time_samples= [int(float(num) * 1000) for num in raw_time_data if num.strip()]

        if frequency_index + 1 < len(lines):
            raw_frequency_data = lines[frequency_index + 1].strip().split(',') 
            #filtered_frequency_data = [float(num) for num in raw_frequency_data if num.strip()]
            frequency_samples = [int(float(num)) for num in raw_frequency_data if num.strip()]

    except Exception as e:
         print(f"An error occurred: {e}")

    return time_samples, frequency_samples





def attack_detection(time_samples, frequency_samples):
    
    frequency_samples = frequency_samples[1:]
    print("Número de muestras de tiempo:", len(time_samples))
    print("Número de muestras de frecuencia:", len(frequency_samples))
     
    if len(time_samples) != len(frequency_samples):
        raise ValueError("Los arrays de tiempo y frecuencia deben tener el mismo tamaño.")
    
    time_differences = np.diff(time_samples)
    
    if np.any(time_differences == 0):            
        print("Hay diferencias de tiempo cero entre algunas muestras. Se eliminarán duplicados.")
        # Eliminar duplicados consecutivos
        unique_time_samples, unique_indices = np.unique(time_samples, return_index=True)
        time_samples = unique_time_samples
        frequency_samples = frequency_samples[unique_indices]

     # Calcular el intervalo de muestreo promedio
    if len(time_samples) > 1:
        d = np.mean(np.diff(time_samples))
    else:
        raise ValueError("No hay suficientes muestras de tiempo después de eliminar duplicados.")

    if d == 0:
        raise ValueError("El intervalo de muestreo calculado es cero, verifica tus datos de tiempo.")

    N = len(frequency_samples)

    fft_values = fft(frequency_samples)

    # Obtener las frecuencias correspondientes a los valores de la FFT
    fft_frequencies = fftfreq(N, d=(time_samples[1] - time_samples[0]))
    
    # Tomar la magnitud de la FFT
    fft_magnitude = np.abs(fft_values)
    
    threshold = 10
    plt.figure(figsize=(10, 5))
    plt.plot(fft_frequencies, fft_magnitude)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.title('FFT de las Frecuencias')
    plt.axhline(y=threshold, color='r', linestyle='--')
    plt.show()

time_samples, frequency_samples = read_and_process_file(file_path)
time_sampes = np.array(time_samples)
frequency_samples = np.array(frequency_samples)
attack_detection(time_samples, frequency_samples)

