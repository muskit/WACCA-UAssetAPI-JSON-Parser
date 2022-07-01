from collections import namedtuple
from encodings import utf_8
import json
from re import M

Song = namedtuple("Song", "id category name artist tempo level level_designer audio")

CATEGORY = {
    '0':'アニメ／ＰＯＰ', #Anime/Pop
    '1':'ボカロ', #Vocaloid
    '2':'東方アレンジ', #Touhou Arrangements
    '3':'2.5次元', #2.5D
    '4':'バラエティ', #Variety
    '5':'オリジナル', #Original
    '6':'TANO*C' #HARDCORE TANO*C
}

## -- JOG AND OUTLIER DATA GOOD FOR "LILY R" --
# pair id to arbitrary audio index without altering idx
SONG_AUDIO_OUTLIERS = {
    'S01-008': 180, #360
    'S01-020': 181, #362
    'S01-049': '???',
    'S01-204': 182, #364
    'S01-209': '???',
    'S01-219': '???',
    'S01-239': '???',
    'S01-240': '???',
    'S01-241': '???',
    'S01-247': 185, #370
    'S01-248': '???',
    'S01-249': '???',
    'S01-251': '???',
    'S01-258': '???',
    'S01-264': '???',
    'S01-267': '???',
    'S02-001': '???',
    'S02-021': [209, 210], #418, 420
    'S02-036': [147, 221], #294, 442
}

# pair id to arbitrary audio index and reseek idx
SONG_AUDIO_JOG = {
    'S01-113': 119, #238
    'S01-117': 101, #202
    'S01-203': 123, #246
    'S01-236': 148, #296
    'S01-250': 156, #312
    'S01-268': 168, #336
    'S02-003': 193, #386
    'S02-023': 211, #422
    'S02-037': 222, #444
}

END_OF_GOOD_RANGE = 'S02-037'

# Build music database as ID-keyed dictionary.
# 
# jsonPath: path to JSON file exported from UAssetGUI
# (Content/Table/MusicParameterTable.uasset)
def get_music_dict(jsonPath: str) -> dict:
    songs = dict()

    f = open(jsonPath, 'r', encoding='utf_8')
    j = json.loads(f.read())
    data = j['Exports'][0]['Table']['Data']

    for elem in data: # songs
        id = ''
        category = ''
        name = ''
        artist = ''
        tempo = -1
        level = [-1, -1, -1, -1]
        level_designer = ['', '', '', '']
        img = ''

        for key in elem['Value']: # properties of song
            if key['Name'] == 'AssetDirectory':
                id = key['Value']
            #SongInfo
            if key['Name'] == 'ScoreGenre':
                category = key['Value']
            if key['Name'] == 'MusicMessage':
                name = key['Value']
            if key['Name'] == 'ArtistMessage':
                artist = key['Value']
            if key['Name'] == 'Bpm':
                tempo = key['Value']
            #ChartInfo Levels
            if key['Name'] == 'DifficultyNormalLv':
                level[0] = key['Value']
            if key['Name'] == 'DifficultyHardLv':
                level[1] = key['Value']
            if key['Name'] == 'DifficultyExtremeLv':
                level[2] = key['Value']
            if key['Name'] == 'DifficultyInfernoLv' and key['Value'] != '+0':
                level[3] = key['Value']
            #ChartInfo Designers
            if key['Name'] == 'NotesDesignerNormal':
                level_designer[0] = key['Value']
            if key['Name'] == 'NotesDesignerHard':
                level_designer[1] = key['Value']
            if key['Name'] == 'NotesDesignerExpert':
                level_designer[2] = key['Value']
            if key['Name'] == 'NotesDesignerInferno':
                level_designer[3] = key['Value']
        
        songs[id] = Song(id, category, name, artist, tempo, level, level_designer, -1)

    # sort songs by ID
    idx = 0
    songs = dict(sorted(songs.items()))

    # assign audio indices
    for song in songs.items():
        if song[1].id in SONG_AUDIO_OUTLIERS:
            songs[song[0]] = song[1]._replace(audio = SONG_AUDIO_OUTLIERS[song[1].id])
        else:
            if song[1].id in SONG_AUDIO_JOG:
                idx = SONG_AUDIO_JOG[song[1].id]
            songs[song[0]] = song[1]._replace(audio = idx)
            idx += 1
    
    return songs

if __name__ == "__main__":
    songs = get_music_dict('data.json')
    # print out songs
    for song in songs.items():
        audio_str = ''
        if type(song[1].audio) == list:
            audio_doubledoffset = []
            for bpm in song[1].audio:
                audio_doubledoffset.append(2*bpm)
            audio_str = f'{song[1].audio} ({audio_doubledoffset})'
        else:
            audio_str = f'{song[1].audio} ({2*song[1].audio})'
        print(f"{song[1].id}: {song[1].name} - {audio_str}")
        if song[1].id == END_OF_GOOD_RANGE:
            print("------ END KNOWN GOOD AUDIO ------\n")