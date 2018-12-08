# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import requests
import sys
from bs4 import BeautifulSoup


def search_lyric_url(song_name):
    """
        Searches the song name on google. If lyric finds on given sites, returns link.
        ** Only searches within the sites given below.
            - Metrolyrics.com
            - Genius.com
            - Azlyrics.com

        Params:
            song_name (string) -- name of the song to be search
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
         }
    url = 'https://www.google.com/search?q=' + song_name.replace(' ','+') + \
                "+Lyrics"+\
                "+site:metrolyrics.com"+\
                "+OR+site:genius.com+"+\
                "OR+site:azlyrics.com" + '&start=0'
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('div', class_='r')
    if len(links) > 0:
        link = links[0].find('a', attrs={'class': None}).get('href')  # only main links on google except sub links
        return link
    else:
        return None

def retrieve_lyric(url):
    """
        Retrieves the lyrics in url given as parameter.
        ** Only searches within the sites given below.
            - Metrolyrics.com
            - Genius.com
            - Azlyrics.com

        Params:
            url (string) -- url of site who have lyric
    """
    req = requests.get(url)
    req.encoding = 'utf-8' # ISO-8859-1 to utf-8
    soup = BeautifulSoup(req.text,'html.parser')
    try:
        if "genius.com" in url:
            return soup.find('div', class_='lyrics').find('p').text
        elif "azlyrics.com" in url:
            return soup.find('div', id=None, class_=None).text
        elif "metrolyrics.com" in url:
            metrolyric = soup.find('div', id='lyrics-body-text').find_all('p', class_='verse')
            return ' \n\n'.join([lyric.text for lyric in metrolyric])
    except :
        print("///////")
        print(sys.exc_info()[0])
        print("///////")
        return None

def lyric_main(song_name):
    """
        Example use of:
            - lyric = lyric_main("Rammstein Stripped ")
            - print(lyric)
    """
    url = search_lyric_url(song_name)
    if url == None: # if url is not found
        url = 'Url not found'
        lyric = 'Lyric not found for {}'.format(song_name)
    else:
        lyric = retrieve_lyric(url)
        if lyric == None: # if lyric is not found
            lyric = 'Lyric not found for {}'.format(song_name)
    return [lyric, url]
