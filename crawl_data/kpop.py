import os
import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

*** !!! IMPORTANT !!! *****************************
First, create 'melon' directory and manually save the 10 webpages (see the URL below)
to the 'melon' directory as 'year.htm'. Save years 2008 - 2017 (10 years worth).

e.g., Save 'https://www.melon.com/chart/age/list.htm?chartGenre=KPOP&chartDate=2012' as melon/2012.htm

After saving 10 webpages (years: 2008--2017), execute this code.

***************************************************

First, this code parses the saved melon webpages that carry 
k-pop yearly ranking (top 100 songs per year) information for 
songs, artists, and lyrics' links*.
(* Links are expressed as lyric ids in the URL.)

Next, this code parses the individual lyric text from melon website.

'''

'''
|+++++++++++++++++++|
| fetch_song_info() |
|+++++++++++++++++++|

parse through the saved 'https://www.melon.com/chart/...' webpages
in the 'melon' directory to fetch k-pop song information:
- ranking
- song name (i.e., song title)
- artist name
- URL (for downloading the lyrics)
- year (when the song was ranked as top-100)

'''

def fetch_song_info():

    # Create 'ranking' directory if there isn't any.

    ranking_dir = 'ranking/'
    if not os.path.exists(ranking_dir):
        os.makedirs(ranking_dir)

    # 10 years worth of top 100 lyrics are processed. (A total of 1,000 lyrics.)

    frames = []
    for year in range(2008, 2018):

        # Read html source

        file_name = 'melon/' + str(year) + '.htm'
        with open(file_name, 'r') as f:
            html = f.read()

        # Extract 100 songs/artist pair per year

        soup = BeautifulSoup(html, 'html.parser')

        songs = soup.find_all('a', attrs={'title': '곡정보 보기'})
        artists = soup.find_all('div', attrs={'class': 'ellipsis rank02'})
        rankings = soup.find_all('span', attrs={'class': 'rank'})

        song_list = []
        song_id_list = []
        for s in enumerate(songs):
            num = re.findall(r'\d+', s[1]['onclick'])
            song_id_list += num
            s_name = re.sub(' 상세정보 페이지 이동', '', s[1].find('span').string)
            song_list.append(s_name)

        artist_list = []
        for a in enumerate(artists):
            artist_list.append(a[1].find('a').string)

        ranking_list = []
        for r in enumerate(rankings):
            ranking_list.append(int(r[1].string))

        print(song_list); print(len(song_list))
        print(artist_list); print(len(artist_list))
        print(song_id_list); print(len(song_id_list))
        print(ranking_list); print(len(ranking_list))

        df = pd.DataFrame({
            'Ranking': ranking_list,
            'SongName': song_list,
            'ArtistName': artist_list,
            'URL' : song_id_list,
            'Year': year
        })
        frames.append(df)

    print("Total webpages parsed:", len(frames))
    result = pd.concat(frames)

    # Save the k-pop ranking result in csv format under 'ranking' directory.

    result.to_csv('ranking/kr_ranking_url.csv', index=False)

'''

|+++++++++++++++++++++++|
| fetch_each_lyric(url) |
|+++++++++++++++++++++++|

crawls each k-pop lyric text from the melon website using
the lyrics ids listed in 'ranking/kr_ranking_url.csv'.

'''

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_each_lyric(url):
    assert isinstance(url, str), 'URL must be a string'
    # Melon website seems to refuse connection over time, so
    # enough time gap of 10 seconds is set to prevent ConnectionError.
    time.sleep(10)

    lyrics_url = url
    try:
        response = requests.get(lyrics_url, headers=USER_AGENT)
        soup = BeautifulSoup(response.content, 'html.parser')
        lyrics_area = soup.find('div', attrs={'class': 'lyric'})

        if lyrics_area != None:
            lyrics = lyrics_area.get_text(separator='\n')
            lyrics = lyrics.strip()
            return lyrics
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection refused"

'''

|++++++++++++++++|
| crawl_lyrics() |
|++++++++++++++++|

crawls all 1,000 lyrics from the melon website using
the lyrics ids listed in 'ranking/kr_ranking_url.csv'.

'''

def crawl_lyrics():

    # Create 'lyrics_kr' directory, if there is none, for storing lyrics.

    kr_dir = "lyrics_kr"
    if not os.path.exists(kr_dir):
        os.makedirs(kr_dir)

    # Read the lyrics ids from 'ranking/kr_ranking_url.csv'.

    df = pd.read_csv('ranking/kr_ranking_url.csv')
    # print(df.shape)
    # df = df.dropna()
    # print(df.shape)   # There are no null or nan in '.csv' file.

    url_list = []  # This list actually stores the lyrics ids given by the melon website.
    lyrics_list = []
    for i, row in df.iterrows():
        url = row['URL']
        print(url)
        url_list.append(url)
        url = "https://www.melon.com/song/detail.htm?songId={}".format(url)
        lyrics = fetch_each_lyric(url)
        lyrics_list.append(lyrics)

    df = pd.DataFrame({
        'Lyrics': lyrics_list,
        'URL': url_list
    })

    # Save crawled k-pop lyrics to file.

    df.to_csv('lyrics_kr/kr_lyrics.csv', index=False)


# Execute the below functions in a sequential order, i.e.,
# fetch_song_info() must precede crawl_lyrics().

fetch_song_info()

crawl_lyrics()
