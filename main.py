from pydub import AudioSegment
from pydub import silence as sn
import os
import librosa, pydub
import numpy as np
import pickle
from parts_detections import vocal_detection, silences_detection
from replacements import replace_vocals
import adjust_tempo as at
import adjust_volume as av
import parts_of_song_extraction as pse
import split_voc_accompaniament as vacc
from chromogram import extract_chromogram
from mfcc import extract_mfcc
import matplotlib.pyplot as plt
import librosa.display
import librosa
from IPython.display import Audio, display
import soundfile as sf
import ruptures as rpt
import beat_tracker as bt
import sys



# sped_acc_1 = r".\sepearated_songs\speed_good4u\accompaniment.wav"
# sped_vocal_1 = r".\sepearated_songs\speed_good4u\vocals.wav"
# sped_vocal_2 = r".\sepearated_songs\speed_stillintoU\vocals.wav"
# sped_acc_sound_1 = AudioSegment.from_wav(sped_acc_1)
# sped_voc_sound_1 = AudioSegment.from_wav(sped_vocal_1)
# sped_voc_sound_2 = AudioSegment.from_wav(sped_vocal_2)
# sped_vocals1 = vocal_detection(sped_voc_sound_1)
# sped_vocals2 = vocal_detection(sped_voc_sound_2)
#
#
# output = replace_vocals(sped_vocals1, sped_vocals2, sped_voc_sound_1, sped_voc_sound_2, sped_acc_sound_1, 7)
# output.export("vocal_replace_good4u_stillintou.wav", format="wav")

# chroma = extract_chromogram(r'C:\Users\aleks\Pulpit\pythonProject\music_mashup_app\venv\songs\paramore_misery_business.mp3')
# print(chroma)
# plt.figure(figsize=(10, 4))
# librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')
# plt.colorbar()
# plt.title('Chromagram')
# plt.tight_layout()
# plt.show()

#
# my_mfcc = extract_mfcc(r'C:\Users\aleks\Pulpit\pythonProject\music_mashup_app\venv\songs\Paramore-StillIntoYou.wav')
# print(my_mfcc)
# plt.figure(figsize=(10, 4))
# librosa.display.specshow(my_mfcc, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
# plt.tight_layout()
# plt.show()


# signal1= AudioSegment.from_mp3(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs'
#                                r'\Katy_Perry_-_All_You_Need_Is_Love_(Clean).mp3')
#
# signal2 = AudioSegment.from_mp3(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs"
#                                 r"\Taylor_Swift_ft_Ed_Sheeran_-_Run_(Taylor's_Version)_(From_The_Vault)_(Clean).mp3")

# signal1, sr = librosa.load(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs'
#                                r'\Katy_Perry_-_All_You_Need_Is_Love_(Clean).mp3')
#
# signal2, sr = librosa.load(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs"
#                                 r"\Taylor_Swift_ft_Ed_Sheeran_-_Run_(Taylor's_Version)_(From_The_Vault)_(Clean).mp3")

sr = 22050

# na razie nieważne
# v_signal1, v_signal2 = av.adjust_volume(signal1, signal2)
# print(type(v_signal1))

# tempo adjustment
# t_signal1, t_signal2 = at.time_stretcher(signal1, signal2)
# print(type(t_signal1))

# # t_signal1.export(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\KatyPerry_alluneed_tv.mp3', format="mp3")
# sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\KatyPerry_alluneed_tv.wav', t_signal1, sr, format='wav')
#
# # t_signal2.export(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\TaylorSwift_EdSheeran_Run_tv.mp3', format="mp3")
# sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\TaylorSwift_EdSheeran_Run_tv.wav', t_signal2, sr, format='wav')


# # Song parts segmantation
# pse.plot_envelope(signal1)
# signal_tempogram = pse.generate_tempogram(signal1)
# changes_number = pse.number_of_changes_in_song(signal_tempogram)
# signal_segments = pse.split_segments('all_u_need_is_love', signal1, changes_number)
#
#
# # Split vocals and accompaniament
# # vacc.split_stems(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\TaylorSwift_EdSheeran_Run_tv.wav', 'decomposition', 5)
# vacc.split_stems(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\KatyPerry_alluneed_tv.wav', 'decomposition4', 4)
# vacc.split_stems(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\TaylorSwift_EdSheeran_Run_tv.wav', 'decomposition4', 4)


# # beats tracking
# signal1, sr = librosa.load(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\KatyPerry_alluneed_tv\other.wav')
#
# signal2, sr = librosa.load(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\TaylorSwift_EdSheeran_Run_tv\other.wav")
#
# sound_with_beats1, beats1 = bt.beat_track_dynamic(signal1, sr)
# sound_with_beats2, beats2 = bt.beat_track_dynamic(signal2, sr)
#
# # sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\beat_songs\KatyPerry_alluneed_beats.wav', sound_with_beats, sr, format='wav')
# # sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\beat_songs\KatyPerry_alluneed_just_beats.wav', beats, sr, format='wav')
#
# beat_start1 = bt.find_beats_start(beats1)[0]
# beat_start2 = bt.find_beats_start(beats2)[0]
#
# new_song1, new_song2 = bt.overlay_beat_songs(signal1, signal2, beat_start1, beat_start2)
#
# sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\moved_songs\KatyPerry_alluneed_to_Taylor_Ed_run.wav', new_song1, sr, format='wav')
# sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\moved_songs\Taylor_Ed_run_to_KatyPerry_alluneed.wav', new_song2, sr, format='wav')
#
#
# sound1 = AudioSegment.from_file(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\moved_songs\KatyPerry_alluneed_to_Taylor_Ed_run.wav')
# sound2 = AudioSegment.from_file(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\moved_songs\Taylor_Ed_run_to_KatyPerry_alluneed.wav')
#
# combined = sound1.overlay(sound2)
#
# bass1 = AudioSegment.from_file(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\TaylorSwift_EdSheeran_Run_tv\bass.wav')
# drums2 = AudioSegment.from_file(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\KatyPerry_alluneed_tv\drums.wav')
#
# combined = combined.overlay(bass1)
# combined = combined.overlay(drums2)

vocal_1 = AudioSegment.from_wav(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition2\KatyPerry_alluneed_tv\vocals.wav")
vocal_2 = AudioSegment.from_wav(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition2\TaylorSwift_EdSheeran_Run_tv\vocals.wav")
# vocal_1_arr, sr = librosa.load(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\KatyPerry_alluneed_tv\vocals.wav")
# vocal_2_arr, sr = librosa.load(r"C:\Users\aleks\Pulpit\app_mashup_music\venv\decomposition4\TaylorSwift_EdSheeran_Run_tv\vocals.wav")

vocals1 = vocal_detection(vocal_1)
vocals2 = vocal_detection(vocal_2)

print(vocals1.fragments[0])
print(vocals1.fragments[1])
print(vocals2.fragments[0])
print(vocals2.fragments[1])

# print(len(vocals1))
# print(len(vocals2))


# # Song parts segmantation
# signal_tempogram1 = pse.generate_tempogram(vocal_1_arr)
# changes_number1 = pse.number_of_changes_in_song(signal_tempogram1)
# signal_segments1 = pse.split_segments('all_u_need_is_love_vocal', vocal_1_arr, changes_number1)
#
# # Song parts segmantation
# signal_tempogram2 = pse.generate_tempogram(vocal_2_arr)
# changes_number2 = pse.number_of_changes_in_song(signal_tempogram2)
# signal_segments2 = pse.split_segments('run_vocal', vocal_2_arr, changes_number2)

# result = [None]*(len(list1)+len(list2))
# result[::2] = list1
# result[1::2] = list2
#
# output = \
# replace_vocals(vocals1, vocals2, vocal_1, vocal_2, 12)

# output.export(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\combined_songs\KatyPerry_Taylor_Ed_alluneed_run_vocals.wav', format='wav')

# combined = combined.overlay(output)
#
# combined.export(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\combined_songs\KatyPerry_Taylor_Ed_alluneed_run.wav', format='wav')
