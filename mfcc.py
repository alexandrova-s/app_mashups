import librosa

def extract_mfcc(path):
    """Extract MFCC from time series using librosa.

    :param signal: (np.ndarray) Audio time series
    :param sr: (int) Sample rate

    :return: (np.ndarray) MFCC sequence
    """

    signal, sample_rate = librosa.load(path)
    mfcc = librosa.feature.mfcc(signal,
                                # n_mfcc=num_coefficients,
                                # n_fft=frame_size,
                                # hop_length=hop_length,
                                sr=sample_rate)
    return mfcc