from similarities import find_similarities, get_indexes_of_minima 

def replace_vocals(voc1, voc2, full_vocal1, full_vocal2, number_of_fragments_to_replace):
    list_of_minima = []
    all_similarities = list(find_similarities(voc1, voc2))
    for x in all_similarities:
        list_of_minima.append(x[1][1])
    print('Minima!!!!!', list_of_minima)
    # index_of_minimum = list_of_minima.index(min(list_of_minima))
    sorted_indexes = get_indexes_of_minima(list_of_minima)
    all_start_moments = []
    all_stop_moments = []
    for index_of_minimum in range(0, len(list_of_minima)):  #sorted_indexes[:number_of_fragments_to_replace]
        to_replace = all_similarities[index_of_minimum]
        all_start_moments.append(to_replace[1][0].stop)
        all_stop_moments.append(to_replace[1][0].start)
    all_start_moments = sorted(all_start_moments)
    all_stop_moments = sorted(all_stop_moments)
    for i in range(0, len(all_start_moments)):
        print(all_start_moments[i])
        print(all_stop_moments[i])
        # print(f"Podmiana w: {to_replace[0].start}")
        # print(to_replace[1][0].stop)
        # vocal_replacement = full_vocal2[to_replace[1][0].stop:to_replace[1][0].start]
    # return vocal_replacement

def replace_vocals_accompaniament(voc1, voc2, full_vocal1, full_vocal2, accompaniament): #, number_of_fragments_to_replace):
    list_of_minima = []
    all_similarities = list(find_similarities(voc1, voc2))
    for x in all_similarities:
        list_of_minima.append(x[1][1])
    print('Minima!!!!!', list_of_minima)
    # index_of_minimum = list_of_minima.index(min(list_of_minima))
    sorted_indexes = get_indexes_of_minima(list_of_minima)
    for index_of_minimum in sorted_indexes[:len(list_of_minima)-1]:
        to_replace = all_similarities[index_of_minimum]
        print(to_replace)
        print(f"Podmiana w: {to_replace[0][0]}")
        vocal_replacement = full_vocal2[to_replace[1][0][0]:to_replace[1][0][1]]
        accompaniament = accompaniament.overlay(vocal_replacement, position=to_replace[0][0])
    return accompaniament


# Mixer
#vocal1
#vocal2
# minima
# co z czym do podmiany
#