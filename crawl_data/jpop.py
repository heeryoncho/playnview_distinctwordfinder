import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code gathers yearly top 100 j-pop song information from the Oricon website.
Note that this code only retrieves song name and artist name;
the lyrics url is not retrieved. (This will be done later.)
 
'''

'''

|++++++++++++++++++++++|
| scrape_web_page(url) |
|++++++++++++++++++++++|

is a general function for executing the HTTP GET request.

'''

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def scrape_web_page(url):
    html = requests.get(url, headers=USER_AGENT, verify=False)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup

'''

|+++++++++++++++++++++++++++++|
| fetch_song_ranking_oricon() |
|+++++++++++++++++++++++++++++|

gathers 1,000+ 10-years worth top-100 j-pop songs from the Oricon website.

'''

def fetch_song_ranking_oricon():
    # Oricon website is crawled using the below url:
    # e.g., 'https://www.oricon.co.jp/rank/js/y/2017/p/10/'

    ranking_url = 'https://www.oricon.co.jp/rank/js/y/'

    # Each Oricon webpage lists 10 songs, so we have to loop 10 times
    # to crawl 100 songs per year.

    frames = []
    for year in range(2008, 2018):
        for page in range(1, 11):
            year_url = ranking_url + str(year) + '/p/' + str(page) + '/'
            print(year_url)

            # Find top 10 songs/artist pair per webpage.

            soup = scrape_web_page(year_url)
            songs = soup.find_all(attrs={'itemprop': 'name'})
            artists = soup.find_all('p', attrs={'class': 'name'})
            rank1 = soup.find_all('p', attrs={'class': 'num '})
            rank2 = soup.find_all('p', attrs={'class': 'num num-s'})
            rankings = rank1 + rank2
            print(songs)
            print(artists)

            song_list = []
            for s in enumerate(songs):
                song_list.append(s[1].string)

            artist_list = []
            for a in enumerate(artists):
                artist_list.append(a[1].string)

            ranking_list = []
            for r in enumerate(rankings):

                ranking_list.append(r[1].string)

            df = pd.DataFrame({
                'Ranking': ranking_list,
                'SongName': song_list,
                'ArtistName': artist_list,
                'Year': year
            })
            print(df)
            frames.append(df)
    len(frames)   # 10 years worth
    result = pd.concat(frames)

    # Save the j-pop ranking result in csv format under 'ranking' directory.

    result.to_csv('ranking/jp_ranking.csv', index=False)


'''

*** !!! IMPORTANT !!! ********************

Because j-pop song titles and artist names are expressed in a variety of ways,
e.g., names of the individual artists are listed for the given music group
instead of the group name, using string match of the artist name and song title
to search for the lyrics can sometimes fail. 
Hence, MANUAL CORRECTIONS were made on some of the song titles and artist names to
better match the lyrics search on the following two websites:

1. http://uta-net.com/
2. http://j-lyric.net/

The manually corrected file is 'ranking/jp_ranking_manually_corrected.csv'.

We use this file instead of 'jp_ranking.csv' file 
to crawl j-pop lyrics from the above two websites.

'''

'''

|++++++++++++++++++++++++++++++++|
| fetch_url_utanet(artist, song) |
|++++++++++++++++++++++++++++++++|

searches a single song's lyric text URL link on the Utanet website.

'''

def fetch_link_utanet(artist, song):
    assert isinstance(artist, str), 'Search term must be a string'
    # Utanet website seems to refuse connection over time, so
    # enough time gap of 10 seconds is set to prevent ConnectionError.
    time.sleep(10)

    uta_url = 'https://www.uta-net.com/search/?Aselect=1&Bselect=1&Keyword={}&sort=4'.format(artist)
    try:
        soup = scrape_web_page(uta_url)
        link = soup.find('a', string=song)
        print(link)
        if link != None:
            lyric_url = link['href']
            return lyric_url
    except requests.exceptions.RequestException as e:
        print(e)

'''

|++++++++++++++|
| first_pass() |
|++++++++++++++|

collects and saves URL links to lyrics texts on the Utanet site.

'''

def first_pass():
    # Manually corrected file is used to increase the chance of finding the lyrics urls.

    df = pd.read_csv('ranking/jp_ranking_manually_corrected.csv')

    year_list = []
    ranking_list = []
    artist_list = []
    song_list = []
    url_list = []
    for i, row in df.iterrows():
        artist = row['ArtistName']
        song = row['SongName']

        # Oricon ranking sometimes lists multiple song titles
        # in a single rank, i.e., tied songs or single titles,
        # and these multiple songs are concatenated using '/'.
        # We use '/' to split the song titles.
        if '/' in song:
            songs = song.split('/')

            for j, s in enumerate(songs):
                artist_list.append(artist)
                song_list.append(s)
                year_list.append(row['Year'])
                ranking_list.append(row['Ranking'])
                link = fetch_link_utanet(artist, s)
                url_list.append(link)
        # Only one song per rank is executed below. (i.e., no '/'.)
        else:
            artist_list.append(artist)
            song_list.append(song)
            year_list.append(row['Year'])
            ranking_list.append(row['Ranking'])
            link = fetch_link_utanet(artist, song)
            url_list.append(link)

    df = pd.DataFrame({
        'Ranking': ranking_list,
        'SongName': song_list,
        'ArtistName': artist_list,
        'Year': year_list,
        'URL': url_list
    })

    # Save utanet url links to file.
    df.to_csv('ranking/jp_ranking_url_utanet.csv', index=False)

    df = df.dropna()  # Remove missing values to see how many links were gathered from the Utanet site.
    print("\nUtanet searched:", df.shape)

'''

|+++++++++++++++++++++|
| fetch_link_jlyric() |
|+++++++++++++++++++++|

searches a single song's lyric text URL link on the J-lyric.net website.

'''


def fetch_link_jlyric(artist, song):
    assert isinstance(artist, str), 'Search term must be a string'
    assert isinstance(song, str), 'Search term must be a string'

    query = 'kt=' + song + '&ct=2&ka=' + artist + '&ca=2&kl=&cl=2'
    escaped_search_term = query.replace(' ', '+')
    # J-lyric.net website seems to refuse connection over time, so
    # enough time gap of 10 seconds is set to prevent ConnectionError.
    time.sleep(10)

    jlyric_url = 'http://search2.j-lyric.net/index.php?{}'.format(escaped_search_term)
    print(jlyric_url)

    try:
        soup = scrape_web_page(jlyric_url)
        links = soup.find_all('p', attrs={'class': 'mid'})
        print(links)
        if links != []:
            lyric_url = links[0].find('a', href=True)
            return lyric_url['href']
    except requests.exceptions.RequestException as e:
        print(e)


'''

|+++++++++++++++|
| second_pass() |
|+++++++++++++++|

collects and saves URL links to lyrics texts on the J-lyric.net site.
*** Note that the second_pass() searches and collects URL links where
the Utanet website failed.

'''

def second_pass():
    # The second pass starts where the 'jp_ranking_url_utanet.csv' left off,
    # and fill in those lyrics URL links that Utanet website failed to collect.

    df = pd.read_csv('ranking/jp_ranking_url_utanet.csv')

    nans = lambda df: df[df.isnull().any(axis=1)]  # Search for missing values.
    missing = nans(df)
    print("\nJ-pop lyrics' URL links that are still missing:", missing.shape)

    year_list = []
    ranking_list = []
    artist_list = []
    song_list = []
    url_list = []
    for i, row in missing.iterrows():
        artist = row['ArtistName']
        song = row['SongName']

        if '/' in song:
            songs = song.split('/')
            for i, s in enumerate(songs):
                artist_list.append(artist)
                song_list.append(s)
                year_list.append(row['Year'])
                ranking_list.append(row['Ranking'])
                link = fetch_link_jlyric(artist, s)
                url_list.append(link)
        else:
            artist_list.append(artist)
            song_list.append(song)
            year_list.append(row['Year'])
            ranking_list.append(row['Ranking'])
            link = fetch_link_jlyric(artist, song)
            url_list.append(link)

    df = pd.DataFrame({
        'Ranking': ranking_list,
        'SongName': song_list,
        'ArtistName': artist_list,
        'Year': year_list,
        'URL': url_list
    })

    df = df.dropna()  # Remove missing values.
    df.to_csv('ranking/jp_ranking_url_jlyrics.csv', index=False)

    print("\nJlyrics searched:", df.shape)


'''

|+++++++++++++++++++++++++++|
| fetch_each_lyric_utanet() |
|+++++++++++++++++++++++++++|

crawls each j-pop lyric from 'https://www.uta-net.com/' using 
the URL links saved at 'ranking/jp_ranking_url_utanet.csv'.

'''

def fetch_each_lyric_utanet(url):
    assert isinstance(url, str), 'URL must be a string'
    time.sleep(10)

    uta_url = 'https://www.uta-net.com{}'.format(url)
    try:
        soup = scrape_web_page(uta_url)
        lyrics_area = soup.find('div', attrs={'id': 'kashi_area'})

        if lyrics_area != None:
            lyrics = lyrics_area.get_text(separator='\n')
            lyrics = lyrics.strip()
            return lyrics
    except requests.exceptions.RequestException as e:
        print(e)



'''

|+++++++++++++++++++++++|
| crawl_lyrics_utanet() |
|+++++++++++++++++++++++|

crawls j-pop lyrics from the utanet website using the
the URL links saved at 'ranking/jp_ranking_url_utanet.csv'.

'''

def crawl_lyrics_utanet():
    # Create 'lyrics_jp' directory if there is none.

    lyrics_jp_dir = "lyrics_jp"
    if not os.path.exists(lyrics_jp_dir):
        os.makedirs(lyrics_jp_dir)

    df = pd.read_csv('ranking/jp_ranking_url_utanet.csv')
    df = df.dropna()
    print("\n# of lyrics to be crawled from Utanet:", df.shape)

    url_list = []
    lyrics_list = []
    for i, row in df.iterrows():
        url = row['URL']
        print(url)
        url_list.append(url)
        lyrics = fetch_each_lyric_utanet(url)
        lyrics_list.append(lyrics)

    df = pd.DataFrame({
        'Lyrics': lyrics_list,
        'URL': url_list
    })

    # Save crawled j-pop lyrics to file.

    df.to_csv('lyrics_jp/jp_lyrics_utanet.csv', index=False)

'''

|++++++++++++++++++++++++++++|
| fetch_each_lyric_jlyrics() |
|++++++++++++++++++++++++++++|

crawls each j-pop lyric from 'http://j-lyric.net/' using 
the URL links saved at 'ranking/jp_ranking_url_jlyrics.csv'.

'''

def fetch_each_lyric_jlyrics(url):

    assert isinstance(url, str), 'URL must be a string'
    time.sleep(10)

    jlyric_url = url
    try:
        soup = scrape_web_page(jlyric_url)
        lyrics_area = soup.find('p', attrs={'id': 'Lyric'})

        if lyrics_area != None:
            lyrics = lyrics_area.get_text(separator='\n')
            lyrics = lyrics.strip()
            return lyrics
    except requests.exceptions.RequestException as e:
        print(e)



'''

|++++++++++++++++++++++++|
| crawl_lyrics_jlyrics() |
|++++++++++++++++++++++++|

crawls j-pop lyrics from the jlyrics.net website using the
the URL links saved at 'ranking/jp_ranking_url_jlyrics.csv'.

'''

def crawl_lyrics_jlyrics():
    # Create 'lyrics_jp' directory if there is none.

    lyrics_jp_dir = "lyrics_jp"
    if not os.path.exists(lyrics_jp_dir):
        os.makedirs(lyrics_jp_dir)

    df = pd.read_csv('ranking/jp_ranking_url_jlyrics.csv')
    df = df.dropna()
    print("\n# of lyrics to be crawled from J-lyric.net:", df.shape)

    url_list = []
    lyrics_list = []
    for i, row in df.iterrows():
        url = row['URL']
        print(url)
        url_list.append(url)
        lyrics = fetch_each_lyric_jlyrics(url)
        lyrics_list.append(lyrics)

    df = pd.DataFrame({
        'Lyrics': lyrics_list,
        'URL': url_list
    })

    # Save crawled j-pop lyrics to file.

    df.to_csv('lyrics_jp/jp_lyrics_jlyrics.csv', index=False)


'''

|++++++++++++++++|
| merge_lyrics() |
|++++++++++++++++|

merges the following two lyrics texts into one.

inputs:
--- lyrics_jp/jp_lyrics_utanet.csv
--- lyrics_jp/jp_lyrics_jlyrics.csv

output:
--- lyrics_jp/jp_lyrics.csv

'''

def merge_lyrics():
    df_utanet = pd.read_csv("lyrics_jp/jp_lyrics_utanet.csv")
    df_utanet = df_utanet.dropna()

    df_jlyrics = pd.read_csv("lyrics_jp/jp_lyrics_jlyrics.csv")
    df_jlyrics = df_jlyrics.dropna()

    df_ja = pd.concat([df_utanet, df_jlyrics], axis=0)

    # Save merged j-pop lyrics to file.
    df_ja.to_csv("lyrics_jp/jp_lyrics.csv", index=None)


# Execute the below functions in a sequential manner.

#---------------------------------------
# Crawl and save top 100 j-pop song name and artist name
# for years 2008 - 2017. (10 years worth)

fetch_song_ranking_oricon()

#---------------------------------------
# Collect j-pop lyrics URL link info. from the Utanet website.

first_pass()

#---------------------------------------
# Collect j-pop lyrics URL link info. from the J-lyric.net website. (Try where Utanet failed.)

second_pass()

#---------------------------------------
# Crawl j-pop lyrics texts from the Utanet website.

crawl_lyrics_utanet()

#---------------------------------------
# Crawl j-pop lyrics texts from the J-lyric.net website. (Try where Utanet left off.)

crawl_lyrics_jlyrics()

#---------------------------------------
# Merge two lyrics csv to one.

merge_lyrics()
