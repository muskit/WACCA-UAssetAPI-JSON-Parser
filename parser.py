from collections import namedtuple
from encodings import utf_8
import json
from re import M

Song = namedtuple("Song", "id category name artist level audio")
songs = []

CATEGORY = {
    '0':'アニメ／ＰＯＰ', #Anime/Pop
    '1':'ボカロ', #Vocaloid
    '2':'東方アレンジ', #Touhou Arrangements
    '3':'2.5次元', #2.5D
    '4':'バラエティ', #Variety
    '5':'オリジナル', #Original
    '6':'TANO*C' #HARDCORE TANO*C
}

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
    'S02-036': 147, #294
}

# where to re-seek the iterator
SONG_AUDIO_JOG = {
    'S01-113': 119, #238
    'S01-117': 101, #202
    'S01-203': 123, #246
    'S01-236': 148, #296
    'S01-250': 156, #312
    'S01-268': 168, #336
    'S02-003': 193, #386
    'S02-023': 211, #422
}

## LAST KNOWN GOOD: S02-024

f = open('data.json', 'r', encoding='utf_8')
j = json.loads(f.read())
data = j['Exports'][0]['Table']['Data']

for elem in data: # songs
    id = ''
    category = ''
    name = ''
    artist = ''
    level = [-1, -1, -1, -1]
    img = ''

    for key in elem['Value']: # properties of song
        if key['Name'] == 'AssetDirectory':
            id = key['Value']
        if key['Name'] == 'ScoreGenre':
            category = key['Value']
        if key['Name'] == 'MusicMessage':
            name = key['Value']
        if key['Name'] == 'ArtistMessage':
            artist = key['Value']
        if key['Name'] == 'DifficultyNormalLv':
            level[0] = key['Value']
        if key['Name'] == 'DifficultyHardLv':
            level[1] = key['Value']
        if key['Name'] == 'DifficultyExpertLv':
            level[2] = key['Value']
        if key['Name'] == 'DifficultyInfernoLv' and key['Value'] != '+0':
            level[3] = key['Value']
    
    songs.append(Song(id, category, name, artist, level, -1))

# sort songs by ID and assign audio indices
idx = 0
songs.sort(key=lambda song: song.id)
for song in songs:
    if song.id in SONG_AUDIO_OUTLIERS:
        song = song._replace(audio = SONG_AUDIO_OUTLIERS[song.id])
    else:
        if song.id in SONG_AUDIO_JOG:
            idx = SONG_AUDIO_JOG[song.id]
        song = song._replace(audio = idx)
        idx += 1

    print(f"{song.id}: {song.name} - {song.audio} ({2*song.audio})")