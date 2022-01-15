import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio, display
import soundfile as sf
import ruptures as rpt  # our package

def fig_ax(figsize=(15, 5), dpi=150):
    """Return a (matplotlib) figure and ax objects with given size."""
    return plt.subplots(figsize=figsize, dpi=dpi)

def plot_envelope(signal, sr=22050):
    # look at the envelope
    fig, ax = fig_ax()
    ax.plot(np.arange(signal.size) / sr, signal)
    ax.set_xlim(0, signal.size / sr)
    ax.set_xlabel("Time (s)")
    _ = ax.set(title="Sound envelope")

def generate_tempogram(signal, sr=22050):

    hop_length_tempo = 256
    # Compute the onset strength

    oenv = librosa.onset.onset_strength(
        y=signal, sr=sr, hop_length=hop_length_tempo
    )
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(
        onset_envelope=oenv,
        sr=sr,
        hop_length=hop_length_tempo,
    )
    # Display the tempogram
    fig, ax = fig_ax()
    _ = librosa.display.specshow(
        tempogram,
        ax=ax,
        hop_length=hop_length_tempo,
        sr=sr,
        x_axis="s",
        y_axis="tempo",
    )
    plt.show()
    return tempogram

def get_sum_of_cost(algo, n_bkps) -> float:
    """Return the sum of costs for the change points `bkps`"""
    bkps = algo.predict(n_bkps=n_bkps)
    return algo.cost.sum_of_costs(bkps)

def number_of_changes_in_song(tempogram, n_bkps_max=20, sr=22050):
    hop_length_tempo = 256
    # Choose detection method
    algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)

    # Choose the number of changes (elbow heuristic)
    # Start by computing the segmentation with most changes.
    # After start, all segmentations with 1, 2,..., K_max-1 changes are also available for free.
    _ = algo.predict(n_bkps_max)

    array_of_n_bkps = np.arange(1, n_bkps_max + 1)

    fig, ax = fig_ax((7, 4))
    ax.plot(
        array_of_n_bkps,
        [get_sum_of_cost(algo=algo, n_bkps=n_bkps) for n_bkps in array_of_n_bkps],
        "-*",
        alpha=0.5,
    )
    ax.set_xticks(array_of_n_bkps)
    ax.set_xlabel("Number of change points")
    ax.set_title("Sum of costs")
    ax.grid(axis="x")
    ax.set_xlim(0, n_bkps_max + 1)

    # Visually we choose n_bkps=5 (highlighted in red on the elbow plot)
    n_bkps = 5
    _ = ax.scatter([5], [get_sum_of_cost(algo=algo, n_bkps=5)], color="r", s=100)

    # Segmentation
    bkps = algo.predict(n_bkps=n_bkps)
    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sr, hop_length=hop_length_tempo)

    # Displaying results
    fig, ax = fig_ax()
    _ = librosa.display.specshow(
        tempogram,
        ax=ax,
        x_axis="s",
        y_axis="tempo",
        hop_length=hop_length_tempo,
        sr=sr,
    )

    for b in bkps_times[:-1]:
        ax.axvline(b, ls="--", color="white", lw=4)

    plt.show()
    return bkps_times

def split_segments(song_name, signal, bkps_times, sr=22050, if_save=True):
    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sr * bkps_times).astype(int).tolist()

    i = 1
    all_segments = []
    for (segment_number, (start, end)) in enumerate(
        rpt.utils.pairwise([0] + bkps_time_indexes), start=1
    ):
        segment = signal[start:end]
        print(f"Segment n°{segment_number} (duration: {segment.size/sr:.2f} s)")
        all_segments.append(segment)
        if if_save:
            sf.write(r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs\all_done\segmented\{}_segment_{}.wav'.format(song_name, song_name, i), segment, sr, format='wav')
        i += 1
    return all_segments