from time import sleep
from datetime import datetime
import sys
import requests
import os
import string
import random
from subprocess import Popen, PIPE

def stream_saver(m3u8_link):

    if 'hdstreams.club' in m3u8_link:
        referer = 'http://hdstreams.club'
    if 'footballstream.to' in m3u8_link:
        referer = 'http://footballstream.to'
    if 'weak_spell' in m3u8_link:
        referer = 'http://liveonscore.net/'
    if 'blacktiecdn' in m3u8_link:
        referer = 'http://www.blacktiesports.net'
    if '35.186.229.173' in m3u8_link:
        referer = 'http://f1livegp.me'

    #_name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=8)) + '.ts'
    tn = datetime.now()
    dt_str = '{}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(tn.year, tn.month, tn.day, tn.hour, tn.minute, tn.second)
    _name = '{}_{}.ts'.format(dt_str, m3u8_link.split('/')[-2])
    full_path = os.path.join(video_dir, _name)

    m3u8_folder = '/'.join(m3u8_link.split('/')[:-1]) + '/'

    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }

    player_started = False
    downloaded = []
    dl_bytes = 0
    runs = 0
    try:
        while True:
            if runs % 8 == 0:
                print('{}, {}, {:.2f} MB'.format(m3u8_link, _name, dl_bytes / 1024 / 1024))
            r = requests.get(m3u8_link, headers=headers, verify=False)
            m3u8_file = r.content.decode()
            sleep(1)
            #print(m3u8_file)
            try: sleep_time = float(m3u8_file.split('#EXTINF:')[-1].split(',')[0])
            except: sleep_time = 3

            if '404 Not Found' in m3u8_file:
                print(m3u8_file)
                return

            lines = [l.strip() for l in m3u8_file.split('\n') if l.strip()]
            to_download = []
            for line in lines:
                #if line.endswith('.ts'):
                if '.ts' in line:
                    if not '://' in line:
                        line = m3u8_folder + line
                        if line not in downloaded:
                            to_download.append(line)
                if '#EXT-X-MEDIA-SEQUENCE' in line:
                    print(line, end='', flush=True)
            print(' ... {}'.format(len(to_download)))
            for x in to_download:
                if len(downloaded) == 21:
                    del downloaded[0]

                with requests.get(x, headers=headers, stream=True, verify=False) as r:
                    if len(r.content) > 1000:
                        print('[{:.2f} MB] {}'.format(len(r.content) / 1024 / 1024, x.split('/')[-1]).split('?')[0])
                        with open(full_path, 'ab') as f:
                            f.write(r.content)
                        downloaded.append(x)
                        dl_bytes += len(r.content)
                    else:
                        print('[{}] Bad GET: {}'.format(len(r.content), x.split('/')[-1]))
                        break

            if len(downloaded) > 3 and not player_started:
                Popen(['vlc', full_path], stdout=PIPE, stderr=PIPE)
                #o, e = p.communicate()
                player_started = True

            runs += 1
            sleep(sleep_time - 1)

    except KeyboardInterrupt:
        #os.remove(full_path)
        sys.exit()

def weak_spell_check():
    streams = [
        'BTESPN',
        'BTS1',
        'BTS2',
        'BTS3',
        'Bein',
        'CNBC',
        'ESPNN',
        'FS1',
        'FS2',
        'LLTV',
        'NBCSN',
        'NBC',
        'PS1',
        'PS2',
        'SSF',
        'SSME',
        'TNT'
    ]
    headers = {'Referer': 'http://liveonscore.net/'}
    alives = []
    for s in streams:
        stream_link = 'http://weak_spell.carniferou.club/edge/{}/chunks.m3u8'.format(s)
        #stream_link = 'http://35.244.255.239/edge/{}/chunks.m3u8'.format(s)
        
        r = requests.get(stream_link, headers=headers)
        if r.status_code != 404:
            #print(r.status_code, stream_link)
            alives.append(stream_link)
        sleep(0.1)
    return alives

def footballstream_io():
    headers = {'Referer': 'http://footballstream.to'}
    alives = []
    for i in range(1, 6):
        stream_link = 'http://cdn2.footballstream.to/live/S{}0/index.m3u8'.format(i)
        #stream_link = 'http://35.244.255.239/edge/{}/chunks.m3u8'.format(s)
        
        r = requests.get(stream_link, headers=headers)
        if r.status_code != 404:
            #print(r.status_code, stream_link)
            alives.append(stream_link)
        sleep(0.1)
    return alives

def hdstreams_club():
    headers = {'Referer': 'http://hdstreams.club'}
    # alives = []
    # for i in range(1, 11):
    #     stream_link = 'http://cdn6.hdstreams.club/live/abr_ch{}/live/ch{}/chunks.m3u8'.format(i, i)
    #     stream_link += '?wmsAuthSign=c2VydmVyX3RpbWU9Ny8xOC8yMDIwIDc6MTE6NDkgQU0maGFzaF92YWx1ZT02cEpzKzMwbnRvcGNKZ2ppZlpQMGpnPT0mdmFsaWRtaW51dGVzPTcyMCZpZD0yMDAxOjdkMDo4YjFmOjlhODA6ZjVjZTpjM2Y5OjNjN2U6ZGFhOCZzdHJtX2xlbj01'
    #     r = requests.get(stream_link, headers=headers)
    #     if r.status_code != 404:
    #         #print(r.status_code, stream_link)
    #         alives.append(stream_link)
    #     sleep(0.1)
    # return alives
    alives = []
    for i in range(1, 11):
        stream_link = 'http://cdn1.hdstreams.club/live/ch{}/index.m3u8'.format(i)
        r = requests.get(stream_link, headers=headers)

        # r = requests.get('http://hdstreams.club/page/ch{}.php'.format(i))
        
        # print(r.content.decode())

        # sys.exit()
        
        # try: stream_link = r.content.decode().split('player.load({source: \'')[1].split('\'')[0]
        # except: continue
        # stream_link = stream_link.replace('live/abr_ch{}/'.format(i), 'live/abr_ch{}/live/ch{}/'.format(i, i)).replace('playlist', 'chunks')
        # r = requests.get(stream_link, headers=headers)
        if r.status_code == 200:
            alives.append(stream_link)
    return alives

video_dir = 'output'
headers = {
    'Referer': 'http://f1livegp.me',
    'User-Agent': 'User-Agent Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# http://cdn4.hdstreams.club/live/abr_ch10/live/ch10/chunks.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9Ny8xOC8yMDIwIDc6MTE6NDkgQU0maGFzaF92YWx1ZT02cEpzKzMwbnRvcGNKZ2ppZlpQMGpnPT0mdmFsaWRtaW51dGVzPTcyMCZpZD0yMDAxOjdkMDo4YjFmOjlhODA6ZjVjZTpjM2Y5OjNjN2U6ZGFhOCZzdHJtX2xlbj01
# http://cdn4.hdstreams.club/live/abr_ch10/live/ch10/playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9Ny8xOC8yMDIwIDc6NDQ6MTUgQU0maGFzaF92YWx1ZT14NjZmNTY0c01qWmtFUlRiS2x0OEtRPT0mdmFsaWRtaW51dGVzPTcyMCZpZD04OS4xMzUuMjAxLjEwMyZzdHJtX2xlbj01

# vlc http://cdn6.hdstreams.club/live/abr_ch5/live/ch5/chunks.m3u8 :http-referrer="hdstreams.club" :http-user-agent="User-Agent Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"

#stream_saver('http://cdn1.hdstreams.club/live/ch10/index.m3u8')
#stream_saver('http://weak_spell.carniferou.club/edge/SSF/chunks.m3u8')
#stream_saver('http://45.134.21.230:8081/abr/abr-K-1/hls/K-1/chunks.m3u8?nimblesessionid=7853117')
#stream_saver('http://cdn7.hdstreams.club/live/abr_ch8/live/ch8/chunks.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9Ny8xNi8yMDIwIDM6NTU6MjUgUE0maGFzaF92YWx1ZT1wNGRIdUtWb1E3czZqaW5YVXMzdSt3PT0mdmFsaWRtaW51dGVzPTcyMCZpZD04My4yNDMuMTQ4Ljc3JnN0cm1fbGVuPTU=')
#sys.exit()

#alives = footballstream_io() + weak_spell_check() + hdstreams_club()
alives = hdstreams_club()

i = 1
choice_dict = {}
for a in alives:
    print('{}. {}'.format(i, a.split('?')[0]))
    #print('{}. {}'.format(i, a))
    choice_dict[i] = a
    i += 1
the_choice = int(input(': '))
stream_saver(choice_dict[the_choice])

#stream_saver('http://35.186.229.173/live/CH2/index.m3u8')
#stream_saver('http://yolu.blacktiecdn.xyz/live/CH1/index.m3u8')
