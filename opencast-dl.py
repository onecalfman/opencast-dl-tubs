#!/usr/bin/python3

import datetime
import json
import requests
import urllib
import os
import pandas
from sys import exit
from tqdm import tqdm

link='https://opencast-present.rz.tu-bs.de/search/episode.json'         # link to episodes.json filename of your OpenCast website. Probably something like
                # https://opencast-present.<your universities website>.de/search/episode.json
json_file = 'test.json'  # location for the downloaded json filename
filename = 'test.csv'   # location of the created csv (should end with .csv).
tmp_file = 'test.tmp'   # Temporary filename because i didn't manage to merge two filenames in python and did it with unix shell
auto_download_file = '.data/opencast-auto-download'
"""
auto download will has to be a plain text filename with the following syntax

series_id,full_path

example:

b5ddb1cc-3e8e-435b-aaed-1712b5b14aed,/home/jonas/tu/fem/
665a4876-1f24-4c59-b69e-170698d6ce34,/home/jonas/tu/messtechnik/video
"""


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

#download_url(link, json_file)

counter = 1
errors = 0
loop = 0
table = []
table_out = []

json_data = json.load(open(json_file))

for result in json_data['search-results']['result']:
    table.append([])
    table[loop].append(str(result['mediapackage']['seriestitle']))
    table[loop].append(str(result['mediapackage']['title']))
    try:
        table[loop].append(result['dcCreator'])
    except:
        table[loop].append('')
    try:
        table[loop].append(result['dcCreated'][:10])
    except:
        table[loop].append('')

    table[loop].append(str(datetime.timedelta(seconds=int(str(result['mediapackage']['duration'])[:-3]))))
    table[loop].append(result['mediapackage']['series'])

    for q in result['mediapackage']['media']['track']:
        table[loop].append(q['tags']['tag'][0])

    for u in result['mediapackage']['media']['track']:
        table[loop].append(u['url'])

    loop += 1

header = ['Serientite', 'Titel', 'Creator', 'Datum', 'Dauer', 'Serie', '360p', '720p', '360p 2', '720p 2']

# The following loop sorts the videos in the already generated matrix by quality
for line in table:
    order = []

    for cell in line:
        if '360p-quality' in cell:
            order.append(0)
        if '720p-quality' in cell:
            order.append(1)
    try:
        if len(order) == 2:
            if order[0]:
                line[6] = line.pop()
                line[7] = line.pop()
            else:
                line[7] = line.pop()
                line[6] = line.pop()
        elif order[0] and order[1]:
            line[8] = line.pop()
            line[6] = line.pop()
            line[9] = line.pop()
            line[7] = line.pop()
        elif order[0] and order[2]:
            line[8] = line.pop()
            line[9] = line.pop()
            line[6] = line.pop()
            line[7] = line.pop()
        elif order[0] and order[3]:
            line[9] = line.pop()
            line[8] = line.pop()
            line[6] = line.pop()
            line[7] = line.pop()
        elif order[1] and order[2]:
            line[8] = line.pop()
            line[9] = line.pop()
            line[7] = line.pop()
            line[6] = line.pop()
        elif order[1] and order[3]:
            line[9] = line.pop()
            line[8] = line.pop()
            line[7] = line.pop()
            line[6] = line.pop()
        elif order[2] and order[3]:
            line[9] = line.pop()
            line[7] = line.pop()
            line[8] = line.pop()
            line[6] = line.pop()
    except:
        print('Line ' + str(counter) + ' parsing problem')
        print('skipping')
        errors += 1
    counter += 1

if errors:
    print('\n' + str(errors) + ' errors')

df = pandas.DataFrame(table)

# This part merges the newly created csv with existing csv if there is a previously downloaded csv filename
try:
    old = sum(1 for line in open(filename))
    df.to_csv(tmp_file, index=False, header=header)
    
    os.system('cat ' + tmp_file + ' ' + filename + ' | grep -v \'Serientitel, Titel, Creator, Datum, Dauer, Serie, 360p, 720p, 360p 2, 720p 2\' | sort -u > /tmp/opencast_merged.csv')
    os.system('mv /tmp/opencast_merged.csv ' + filename)
    os.system('sed -i -e \'s/Ã?/Ü/g\' -e \'s/Ã¼/ü/g\' -e \'s/Ã¤/ä/g\' -e \'1 i\Serientitel,Titel,Creator,Datum,Dauer,Serie,360p,720p,360p 2,720p 2\' ' + filename)
    df.append(pandas.read_csv(filename))
    df = pandas.read_csv(filename)
except:
    old = 0
    df.to_csv(filename, index=False, header=header) # you could output to other formats like xlsx, refere to pandas docs

new = len(df)
print(str(new - old + 1) + ' new entries')
print(str(new) + ' entries total')

# If an auto_download filename was specified the selected series will be downloaded
try:
    auto_download = pandas.read_csv(auto_download_file, header=None).values.tolist()
    print("auto download file found")
except:
    exit("No auto download file found or specified")

for line in auto_download:
    id = line[0]
    selection = df.loc[df['Serie'] == id].values.tolist()
    for row in selection:
        path = line[1] + '/' + row[1] + '.mp4'
        if not os.path.exists(path):
            try:
                print('Downloading ' +  row[0] + ' ' + row[1])
                download_url(row[7], line[1] + '/' + row[1] + '.mp4')
            except:
                print('Failed ' + row[0] + ' ' + row[1]);
