from crawl_data import kpop
from crawl_data import jpop
from crawl_data import lyrics_statistics

'''

# Author: Heeryon Cho <heeryon.cho@gmail.com>
# License: BSD-3-clause

This code crawls J-pop/K-pop lyrics data from Japanese/Korean
music ranking websites and lyrics websites.

'''


# Execute the below functions in a sequential manner.

#----------------------------------------------------------------------------------
# CRAWL K-POP LYRICS DATA
#----------------------------------------------------------------------------------

# Extract yearly top 100 ranking K-pop song information from the
# saved webpages in 'melon' directory.

kpop.fetch_song_info()

# Crawl K-pop lyrics text using URLs (song IDs) extracted from the ranking webpage.
# The crawled lyrics are saved under the 'lyrics_kr' folder.

kpop.crawl_lyrics()


#----------------------------------------------------------------------------------
# CRAWL J-POP LYRICS DATA
#----------------------------------------------------------------------------------

# Crawl and save top 100 j-pop song name and artist name
# for years 2008 - 2017. (10 years worth)

jpop.fetch_song_ranking_oricon()

# Collect j-pop lyrics URL link information from the Utanet website.

jpop.first_pass()

# Collect j-pop lyrics URL link info. from the J-lyric.net website. (Try where Utanet failed.)

jpop.second_pass()

# Crawl j-pop lyrics texts from the Utanet website.

jpop.crawl_lyrics_utanet()

# Crawl j-pop lyrics texts from the J-lyric.net website. (Try where Utanet left off.)

jpop.crawl_lyrics_jlyrics()

# Merge two lyrics csv to one.

jpop.merge_lyrics()


#----------------------------------------------------------------------------------
# JOIN LYRICS DATA WITH SONG INFORMATION
#----------------------------------------------------------------------------------

# Merge lyrics texts with corresponding song information (e.g., SongName, ArtistName, etc.)

lyrics_statistics.integrate_info()

