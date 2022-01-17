from pydub import silence as sn


class Fragment:
    def __init__(self, start, stop, duration):
        self.start = start
        self.stop = stop
        self.duration = duration

class Fragments:
    # fragments = []

    def __init__(self):
        self.fragments = []

    def __len__(self):
        return len(self.fragments)

    def append_fragment(self, start, stop, duration):
        self.fragments.append(Fragment(start, stop, duration))


def silences_detection(sound):
    dBFS = sound.dBFS
    print(dBFS)
    silence = sn.detect_silence(sound, min_silence_len=500, silence_thresh=dBFS-16)

    silence = [(start, stop) for start, stop in silence] #in sec

    return silence


def vocal_detection(sound, time_threshold = 5000):
    dBFS = sound.dBFS
    silence = sn.detect_silence(sound, min_silence_len=500, silence_thresh=dBFS-16)

    silence = [(start, stop) for start, stop in silence]
    # print(silence)
    voice = Fragments()
    for index, x in enumerate(silence):
        try:
            if abs(silence[index][0]-x[1]) > time_threshold:
                voice.append_fragment(x[1], silence[index][0], silence[index][0]-x[1])
        except IndexError as e:
            print('blooooooo')
            return voice
    print('vocal detection complited', type(voice))
    return voice






#Fragments
# lista fragmentow = [fragment, ]
#fragment
# from
# to
# duration

# vocal = vocal_detection(sound, time_threshold = 500) # return Fragments()
# vocal.fragments[0].duration
# pianio = mix_piano(sound, time_threshold = 500) # return Fragments()
# pianio.fragments[0].duration
