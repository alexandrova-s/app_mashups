def create_fragments(song, duration=60000, fragmented_by=6):
    fragment = duration/fragmented_by
    song_elems = []
    for x_time in range(fragmented_by):
        song_elems.append(song[fragment*x_time:fragment*(x_time+1)])
        # wychwytywanie przerw
        # ew inny algorytm do podzialu na fragmenty
        # wysoki i niski dzwiek -> pisk ->
    return song_elems

def take_slice(sound, start, end):
    return sound[start:end]