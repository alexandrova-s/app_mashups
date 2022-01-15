import librosa

def extract_chromogram(path):
    """Extract chromogram from time series using librosa.

    :param signal: (np.ndarray) Audio time series
    :param sr: (int) Sample rate

    :return: (np.ndarray) Chromogram
    """
    signal, sample_rate = librosa.load(path)
    chromogram = librosa.feature.chroma_stft(signal,
                                             # n_fft=frame_size,
                                             # hop_length=hop_length,
                                             sr=sample_rate)
    return chromogram