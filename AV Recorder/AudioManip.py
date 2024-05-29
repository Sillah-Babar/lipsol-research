
from scipy.io import wavfile
import noisereduce as nr
from pyAudioAnalysis import audioBasicIO as aIO
from IPython.display import Audio
from numpy.fft import fft, ifft
import wave
import numpy as np
import wave
import matplotlib.pyplot as plt


def read_audio_file(audio_file_name):
    wav_obj = wave.open(audio_file_name, 'rb')

    rate, data = wavfile.read(audio_file_name)
    # wav_obj = wave.open(audio_file_name, 'rb')

    # Getting the sampling rate
    sample_freq = wav_obj.getframerate()

    # Getting Number of individual frames
    n_samples = wav_obj.getnframes()

    # Getting duration of audio file
    t_audio = n_samples / sample_freq

    # Getting number of channels of sound
    n_channels = wav_obj.getnchannels()

    # Getting amplitude of wave at each frame
    signal_wave = wav_obj.readframes(n_samples)

    # To get signal values from this, we have to turn to numpy

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    # Before we get to plotting signal values, we need to calculate the time at which each sample is taken.
    # This is simply the total length of the track in seconds, divided by the number of samples
    #  We can use linspace() from numpy to create an array of timestamps

    times = np.linspace(0, n_samples / rate, num=n_samples)

    return [data, rate, signal_array, times, t_audio]



# Function which plot amplitude of an audio with time on graph
def display_audio_amp_graph(audio_file_name, nr_flag=True):
    # load data
    [data, rate, signal_array, time_array, duration] = read_audio_file(audio_file_name)
    # rate, data = wavfile.read(audio_file_name)

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)

    signal_array = np.frombuffer(data, dtype=np.int16)
    reduce_signal_array = np.frombuffer(reduced_noise, dtype=np.int16)

    # Plotting audio amplitude plot without Noise
    plt.figure(figsize=(10, 5))

    # nr = noise_reduce
    if nr_flag == True:
        plt.plot(time_array, reduce_signal_array)
    else:
        plt.plot(time_array, signal_array)

    plt.title('Channel Input without NOISE')
    plt.ylabel('Signal Value')
    plt.xlabel('Time (s)')
    plt.xlim(0, duration)
    plt.show()


if __name__ == "__main__":
    audio_file_name = ".\\2\\mkh\\mkh_audio.wav"

    display_audio_amp_graph(audio_file_name, nr_flag=True)
