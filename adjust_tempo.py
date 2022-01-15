from pydub import AudioSegment
from pydub import silence as sn
import os
import librosa, pydub
import numpy as np
import pickle
import pyrubberband as pyrb
import soundfile as sf
import matplotlib.pyplot as plt

def adjust_tempo(path1, song_name1, path2, song_name2, sr=22050):
    if not os.path.exists('cache'):
        os.makedirs('cache')

    Yin = []
    Yout = []
    if os.path.exists("cache/%s.pkl" % song_name1):
        with open(path1, 'rb') as f:
            Yin = pickle.load(f)

    if os.path.exists("cache/%s.pkl" % song_name2):
        with open(path2, 'rb') as f:
            Yout.append(pickle.load(f))

    y1, sr = librosa.load(path1, sr=sr)
    Yin = y1

    y2, sr = librosa.load(path2, sr=sr)
    Yout.append(y2)

    Yout = Yout[0]  # NOTE: considering 1mixin & 1mixout

    tempo1, beats1 = librosa.beat.beat_track(y=Yin, sr=sr)
    tempo2, beats2 = librosa.beat.beat_track(y=Yout, sr=sr)

    print("Tempo1=", tempo1)
    print("Tempo2=", tempo2)

    C = [-2, -1, 0, 1, 2]

    if tempo1 == tempo2:
        tempo_tgt = tempo1
        return # return two songs

    Tin = [(2 ** c) * tempo1 for c in C]
    TinIndex = np.argmin(np.absolute(Tin - tempo2))
    Copt = C[TinIndex]
    Bopt = (2 ** Copt) * tempo1

    Tlow = min(Bopt, tempo2)
    Thigh = max(Bopt, tempo2)

    a, b = 0.765, 1
    Ttgt = (a - b) * Tlow + np.sqrt(((a - b) ** 2) * (Tlow ** 2) + 4 * a * b * Thigh * Tlow)
    Ttgt = Ttgt / (2 * a)

    print("FoptIn=", Ttgt / Bopt)
    print("FoptOut=", Ttgt / tempo2)
    print("Ttgt=", Ttgt)

    tempo_tgt = Ttgt

    sIn = pydub.AudioSegment.from_file(path1, format="wav")
    sOut = pydub.AudioSegment.from_file(path2, format="wav")

    speed1 = round(tempo_tgt/tempo1, 4)
    speed2 = round(tempo_tgt/tempo2, 4)

    print("Playback Speed of first song=",speed1,'X')
    print("Playback Speed of second song=",speed2,'X')

    # sIn = effects.speedup(sIn, playback_speed=speed1)
    # sOut = effects.speedup(sOut, playback_speed=speed2)

    sIn = speed_change(sIn, speed1)
    sOut = speed_change(sOut, speed2)

    return sIn, sOut


def adjust_tempo1(path1, path2, sr=22050):

    y1, sr = librosa.load(path1, sr=sr)

    y2, sr = librosa.load(path2, sr=sr)

    tempo1, beats1 = librosa.beat.beat_track(y=y1, sr=sr)
    tempo2, beats2 = librosa.beat.beat_track(y=y2, sr=sr)

    print("Tempo1=", tempo1)
    print("Tempo2=", tempo2)

    C = [-2, -1, 0, 1, 2]

    if tempo1 == tempo2:
        tempo_tgt = tempo1
        return # return two songs

    Tin = [(2 ** c) * tempo1 for c in C]
    TinIndex = np.argmin(np.absolute(Tin - tempo2))
    Copt = C[TinIndex]
    Bopt = (2 ** Copt) * tempo1

    Tlow = min(Bopt, tempo2)
    Thigh = max(Bopt, tempo2)

    a, b = 0.765, 1
    Ttgt = (a - b) * Tlow + np.sqrt(((a - b) ** 2) * (Tlow ** 2) + 4 * a * b * Thigh * Tlow)
    Ttgt = Ttgt / (2 * a)

    print("FoptIn=", Ttgt / Bopt)
    print("FoptOut=", Ttgt / tempo2)
    print("Ttgt=", Ttgt)

    tempo_tgt = Ttgt

    sound1 = pydub.AudioSegment.from_file(path1, format="wav")
    sound2 = pydub.AudioSegment.from_file(path2, format="wav")

    speed1 = round(Ttgt / Bopt, 4)
    speed2 = round(Ttgt / tempo2, 4)

    print("Playback Speed of first song=", speed2, 'X')
    print("Playback Speed of second song=", speed1, 'X')

    s1 = speed_change(sound1, speed2)
    s2 = speed_change(sound2, speed1)

    return s1, s2

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)})
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def audiosegment_to_librosawav(audiosegment):
    channel_sounds = audiosegment.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]

    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max
    fp_arr = fp_arr.reshape(-1)

    return fp_arr

def time_stretcher(sound1, sound2, sr=22050):
    # sound1 = audiosegment_to_librosawav(sound1)
    # sound2 = audiosegment_to_librosawav(sound2)

    tempo1, beats1 = librosa.beat.beat_track(y=sound1, sr=sr)
    tempo2, beats2 = librosa.beat.beat_track(y=sound2, sr=sr)

    print('BPM1: ', tempo1)
    print('BPM2: ', tempo2)

    middle_bpm = (tempo1+tempo2)/2

    ratio1 = middle_bpm/tempo1
    ratio2 = middle_bpm/tempo2

    y_stretch1 = pyrb.time_stretch(sound1, sr, ratio1)
    y_stretch2 = pyrb.time_stretch(sound2, sr, ratio2)

    # y_stretch1 = pydub.AudioSegment(
    #     y_stretch1.tobytes(),
    #     frame_rate=sr,
    #     sample_width=4,
    #     channels=1
    # )
    #
    # y_stretch2 = pydub.AudioSegment(
    #     y_stretch2.tobytes(),
    #     frame_rate=sr,
    #     sample_width=4,
    #     channels=1
    # )

    return y_stretch1, y_stretch2

