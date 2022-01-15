import os
path = r'C:\Users\aleks\Pulpit\app_mashup_music\venv\all_songs'
for filename in os.listdir(path):
    #print(filename)
    os.rename(os.path.join(path,filename),os.path.join(path, filename.replace(' ', '_')))