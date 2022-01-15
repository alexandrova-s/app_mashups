# import madmom
# # from madmom import madmom
#
# def rnn_beattrack(sound, sr):
#     # approach 2 - dbn tracker
#     proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
#     act = madmom.features.beats.RNNBeatProcessor()
#
#     beat_times = proc(act)
#
#     clicks = librosa.clicks(beat_times, sr=sr, length=len(sound))
#     # ipd.Audio(x + clicks, rate=sr
#     print(type(sound+clicks))

import librosa
import numpy as np
import sys
import scipy.signal
import matplotlib.pyplot as plt

def beat_track_dynamic(sound, sr):
    tempo, beat_times = librosa.beat.beat_track(sound, sr=sr, start_bpm=60, units='time')
    clicks = librosa.clicks(beat_times, sr=sr, length=len(sound))

    return sound+clicks, clicks

def plot_beats(clicks):
    plt.figure(figsize=(14, 5))
    # librosa.display.waveplot(x, alpha=0.6)
    plt.vlines(clicks, -1, 1, color='r')
    plt.ylim(-1, 1)
    plt.show()

def find_beats_start(clicks):
    clicks_indicies = scipy.signal.find_peaks(clicks)
    return clicks_indicies[0]


def overlay_beat_songs(song1, song2, ind1, ind2, sr=22050):
    if ind1 > ind2:
        diff = ind1 - ind2
        adjusted_song2 = np.concatenate([np.array([0]*diff), song2])
        return song1, adjusted_song2
    else:
        diff = ind2 - ind1
        adjusted_song1 = np.concatenate([np.array([0]*diff), song1])
        return adjusted_song1, song2


