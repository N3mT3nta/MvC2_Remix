import os
from shutil import copyfile, move, rmtree

input_file = 'MvC2.iso'
output_file = 'MvC2_Remix.iso'

musics_folder = 'musics/'
adx_folder_default = 'ADX_files_default/'
adx_folder_modified = 'ADX_files_modified/'

folders = [musics_folder, adx_folder_default, adx_folder_modified]

for folder in folders:
    if not os.path.exists(folder):
        print(f'{folder} not detected. Creating...')
        os.mkdir(folder)

widescreen_patches = (
('06AB0046820B0046803F023C00688244', '06AB0046820B0046AA3F023C00688244'),
('38008EE40800E0033C0083AC0000000000000000A0FFBD27', '38008EE43C0083AC403F033C0800E003000083ACA0FFBD27'),
('82300246AA3F033C', '82300246E33F023C')
)

piso_path = 'bin\\piso\\piso.exe'
ffmpeg_path = 'bin\\ffmpeg.exe'
afspacker_path = 'bin\\AFSPacker.exe'
palmod_path = 'bin\\PalMod\\PalMod.exe'
iso_path = 'MvC2.iso'

piso_args = ffmpeg_args = mkisofs_args = afspacker_args = ''

verbose = False
clean = True

if verbose == False:
    #piso_args = ' > NUL'
    #afspacker_args = ' > NUL'
    ffmpeg_args = ' -loglevel error'


valid_audio_filenames = [
    'adx_s000.adx', 'adx_s010.adx', 'adx_s020.adx', 'adx_s030.adx',
    'adx_s040.adx', 'adx_s050.adx', 'adx_s060.adx', 'adx_s070.adx',
    'adx_s080.adx', 'adx_s090.adx', 'adx_s0a0.adx', 'adx_s0b0.adx',
    'adx_capl.adx', 'adx_open.adx', 'adx_staf.adx', 'adx_selc.adx',
    'adx_cont.adx', 'adx_here.adx', 'adx_over.adx', 'adx_rank.adx',
    'adx_wins.adx', 'adx_menu.adx', 'adx_netw.adx'
]


def clean_env():
    rmtree(adx_folder_default)
    rmtree(adx_folder_modified)
    rmtree('MvC2/')
    os.remove('MvC2_widescreen.iso')

if len(os.listdir(musics_folder)) == 0:
    print('ERROR: musics folder is empty. Aborting...')
    quit()

if input('Apply widescreen patch? [y/N]: ') in 'Yy':
    with open(iso_path, 'rb') as file:
        print('Reading file...')
        file_hex = file.read().hex()
    valid = True
    for patch in widescreen_patches:
        if not patch[0] in file_hex:
            print('HEX value does not match, skipping...')
            break
            valid = False
    if valid:
        with open('MvC2_widescreen.iso', 'wb') as file:
            print('Patching...')
            for patch in widescreen_patches:
                patched_file_hex = file_hex.replace(patch[0], patch[1])
            print('Writing file...')
            file.write(bytes.fromhex(patched_file_hex))
            rename('MvC2.iso', 'MvC2_original.iso')
            iso_path = 'MvC2_widescreen.iso'
    
print('Extracting ISO...')
os.system(f'{piso_path} -y extract {iso_path} / -od MvC2{piso_args}')

print('Getting default audio files...')
os.system(
    f'{afspacker_path} -e MvC2/PS2/AFS00.AFS {adx_folder_default}{afspacker_args}')
audio_files = os.listdir(adx_folder_default)

print('Checking file names...')
for music in os.listdir(musics_folder):
    valid = False
    for item in valid_audio_filenames:
        if item == music.replace('mp3', 'adx'):
            valid = True
    if not valid:
        print(f'{music} is an invalid file name. Aborting...')
        quit()

print('Converting .mp3 to .adx...')

for music in os.listdir(musics_folder):
    adx_name = music.replace('mp3', 'adx')
    music_path = musics_folder + music
    music_converted_path = adx_folder_modified + adx_name

    print(f'    Converting {music}')
    os.system(
        f'{ffmpeg_path}{ffmpeg_args} -stats -y -i {music_path} -ab 432k -ar 48000 {music_converted_path}'
    )

print('Filling folder with default audio files...')
for music in os.listdir(musics_folder):
    music_path = musics_folder + music
    copyfile(music_path, adx_folder_default + music)

print('\nCreating modified AFS00.AFS')
os.system(f'{afspacker_path} -c {adx_folder_modified} AFS00.AFS{afspacker_args}')

print('Moving file to game directory...')
move('AFS00.AFS', './MvC2/PS2/AFS00.AFS')

print('Reconstructing ISO...')
os.system(
    f'{piso_path} create -o {output_file} -add MvC2 / -ot iso -disable-optimization -udf on{piso_args}'
)

if clean:
    print('Cleaning environment...')
    clean_env()

print(f'File saved to {output_file}')
