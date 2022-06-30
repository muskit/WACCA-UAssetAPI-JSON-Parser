from collections import namedtuple
from encodings import utf_8
import json
from re import M

Song = namedtuple("Song", "id category name artist level")
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

SONG_AUDIO_OUTLIERS = {
    'S01-008': 360,
    'S01-020': -1,
    'S01-049': -1
}

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
    
    songs.append(Song(id, category, name, artist, level))

idx = 0
songs.sort(key=lambda song: song.id)
for song in songs:
    if song.id in SONG_AUDIO_OUTLIERS:
        print(f"{song.id}: {song.name} - {SONG_AUDIO_OUTLIERS[song.id]}")
    else:
        print(f"{song.id}: {song.name} - {idx*2}")
        idx += 1