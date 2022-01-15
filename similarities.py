def the_best_similarity(voice, duration_of_fragment_2):
    index = 0
    differences = [abs(fragment.duration-duration_of_fragment_2) for fragment in voice.fragments]
    minimum = min(differences)
    print(f"najbardziej podobne to {minimum} i to {differences.index(minimum)}")
    return voice.fragments[differences.index(minimum)], minimum

def find_similarities(vocals1, vocals2):
    print(type(vocals1))
    print(len(vocals1))
    print(len(vocals2))
    for fragment1 in vocals1.fragments:
        vocal_to_replace = the_best_similarity(vocals2, fragment1.duration)
        yield (fragment1, vocal_to_replace) # (fragment1, (fragment, minimum))

def get_indexes_of_minima(list_of_minima):
    sorted_list = sorted(list_of_minima)
    return [list_of_minima.index(x) for x in sorted_list]