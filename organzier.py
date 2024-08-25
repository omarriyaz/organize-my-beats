import librosa
import os
import pydub
import numpy as np
from pydub import AudioSegment, silence

input_path = "Beats"
output_path = "Beats_Organized"

def remove_silence(file_name):
    # This function removes the first 25 miliseconds of silence from the mp3 file and exports it as a wav file
    # FL studio exports mp3s with 25 miliseconds of silence at the beginning and end of each mp3, this does not apply to wav files

    # Removes the first 25 miliseconds of silence from the mp3 file
    mp3 = AudioSegment.from_file(input_path + "/" + file_name)
    mp3 = mp3[25:]

    # export the mp3 file without the first 25 miliseconds of silence as a wav file
    mp3.export("Beats_Organized/" + beat_name[:-4] + ".wav", format="wav")

def get_bpm(file_name):
    # This function returns the bpm of the wav file

    # y stores the audio time series and sr stores the sampling rate of y
    y, sr = librosa.load(output_path + "/" + file_name)

    # load the tempo tracker to get the estimated tempo of the track
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_intervals = np.diff(beat_times)

    tempos = 60.0 / beat_intervals
    tempo_rounded = np.mean(tempos)
    
    tempo_rounded = round(tempo_rounded)

    if tempo_rounded < 100: tempo_rounded = tempo_rounded * 2

    return str(tempo_rounded)

def get_key(file_name):
    # This function returns the key of the wav file

    # y stores the audio time series and sr stores the sampling rate of y
    y, sr = librosa.load(output_path + "/" + file_name)

    # Compute the Chroma Short-Time Fourier Transform (chroma_stft)
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

    # Calculate the mean chroma feature across time
    mean_chroma = np.mean(chromagram, axis=1)

    # Define the mapping of chroma features to keys
    chroma_to_key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Find the key by selecting the maximum chroma feature
    estimated_key_index = np.argmax(mean_chroma)
    estimated_key = chroma_to_key[estimated_key_index]

    # Print the detected key
    return str(estimated_key)


# convert all mp3 files to wav files
for beat_name in sorted(os.listdir(input_path)):
    if beat_name.endswith(".mp3"):
        remove_silence(beat_name)

# get the bpm of all the wav files
for beat_name in sorted(os.listdir(output_path)):
    if beat_name.endswith(".wav"):
        # rename the file to include the bpm and key
        bpm = get_bpm(beat_name)
        key = get_key(beat_name)
        os.rename(output_path + "/" + beat_name, output_path + "/" + beat_name[:-4] + "_" + bpm + "BPM_" + key + ".wav")