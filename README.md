# organize-my-beats

## Overview

This script automates the process of organizing and labeling beats for music producers. It converts MP3 files to WAV format, removes initial silence added during export from FL Studio, and calculates the BPM (Beats Per Minute) and musical key of each beat. This helps producers quickly provide artists with the necessary details without them having to use external tools to detect the key/tempo.

## Why I made this script

As a music producer using FL Studio, I've built a large catalog of beats over the past three years. When artists ask for a beat's BPM and key, I typically have to open the original project file and use external plugins to find this information. This is time-consuming and interrupts my workflow. To streamline this process, I've created this Python script to automatically process and label my beats with their respective BPM and key.

## How it works

- Convert MP3 to WAV: The script takes any MP3 file from the 'Beats' folder and converts it into a WAV file. This conversion removes the 25 milliseconds of silence that FL Studio adds at the beginning of each exported MP3 file.

- Remove Silence: While converting, the script removes the first 25 milliseconds of silence from the MP3 file, as this is not apart of the actual beat, and could mess up the recording project for the artist.

- Calculate BPM: For each WAV file, the script calculates the BPM using the librosa library. It analyzes the beat frames and converts them to time using the librosa.frames_to_time function. The script then calculates beat intervals using numpy.diff and derives the tempo by computing 60 divided by the number of beat intervals. If the detected tempo is below 100 BPM, it is doubled, as I typically work with tempos in the range of 100-150 BPM. For example the tempo I had set could be 150, but the detected tempo could come to 75, thus I want to double it.

- Determine Key: The script also determines the musical key of each WAV file using a Chroma feature analysis via librosa. It computes the Chroma Short-Time Fourier Transform and calculates the mean chroma feature across time to estimate the most prominent musical key.

- Rename Files: Finally, the script renames each WAV file to include its BPM and key, making it easier to identify and share with artists. These renamed files can be found in the 'Beats_Organized' folder.

## Dependencies

To run this script, you need to install the following Python libraries:

librosa: For audio analysis and feature extraction. Install using pip install librosa.
numpy: For numerical operations. Install using pip install numpy.
pydub: For handling audio file conversion and editing. Install using pip install pydub.
You will also need FFmpeg installed on your system for pydub to handle audio conversions properly.

## Limitations

- Accuracy: The BPM and key detection relies on the accuracy of the librosa library, which may not always align perfectly with manual detection methods or the settings used in FL Studio. From my very limited testing, the accuracy came out to be around 30 - 40%, which is quite low.
- Processing Time: For a large number of files, the processing time may be significant due to audio loading and analysis.
- Initial Silence: The script assumes FL Studio adds exactly 25 milliseconds of silence to all MP3 exports, which may not hold true for other DAWs or export settings.

## Future Work

- Integrate TuneBat: TuneBat offers a much more accurate BPM/Key Prediction, the problem is they do not have an API to use.
- GUI Development: Develop a graphical user interface to turn this into a real tool for producers as most users would not prefer to work with command-line interfaces.
