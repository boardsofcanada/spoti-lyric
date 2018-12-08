# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import config
import os
from spotify_authorization import SpotifyAuthorization
from spoti_lyric import SpotiLyric

def file_check():
    """
        Checks the 'refresh_token.txt' file.
    """
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        file = open(path + '/refresh_token.txt', 'r')
        return True
    except FileNotFoundError:
        return False

if file_check() == False:
    # makes just once authorization
    print("'refresh_token.txt' is not found.")
    print("Authorization is starting...")
    SpotifyAuthorization(config.SPOTIFY_CLIENT_ID,
        config.SPOTIFY_CLIENT_SECRET,
        config.SPOTIFY_REDIRECT_URI,
        config.SPOTIFY_SCOPE).main()
    print("Authorization sucessfully!")

# if authorization made, run main program
print("Program is starting...")
SpotiLyric(config.SPOTIFY_CLIENT_ID,
    config.SPOTIFY_CLIENT_SECRET,
    config.SPOTIFY_REDIRECT_URI,
    config.SPOTIFY_SCOPE)
