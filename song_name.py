# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import os
import requests
import base64

class SongName:
    """
        This class makes requesting to refresh 'access token' when token expired and gets song that is currently playing on Spotify.

        Example use of:
            - s = SongName(client_id, client_secret)
            - song_name = s.main()
            - print(song_name)
    """
    def __init__(self, client_id, client_secret):
        """
            Params:
                client_id -- client id of your API which register to Spotify.
                client_secret -- client secret id of your API which register to Spotify.
        """
        self.spotify_client_id = client_id
        self.spotify_client_secret = client_secret
        self.access_token = ''
        self.song_name = ''
        # assignment the 'refresh token' code from 'refresh token.txt'
        self.refresh_token = self.get_refresh_token_code_from_file()[0].strip()

    def authorization_header_base64(self, client_id, client_secret):
        """
            Makes authorization header.
            Base 64 encoded string that contains the client ID and client secret key.

            Params:
                client_id -- client id of your API which register to Spotify.
                client_secret -- client secret id of your API which register to Spotify.
        """
        header_base64 = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
        header_base64 = str(header_base64).split("'")[1]
        return {'Authorization': 'Basic {}'.format(header_base64)}

    def refresh_access_token(self, refresh_token, header_base64):
        """
            Request to refreshing 'access token'

            Params:
                refresh_token --  the refresh token returned from the authorization code exchange.
                header_base64 -- base 64 encoded string that contains the client ID and client secret key.

            Returns a new 'access token'.
        """
        url = 'https://accounts.spotify.com/api/token'
        body_params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            }
        req = requests.post(url, data=body_params, headers=header_base64)
        if req.status_code == 200:
            return req.json()['access_token']
        else:
            return None

    def authorization_header_bearer(self, access_token):
        """
            Example return:
                - {'Authorization': 'NgCXRK...MzYjw'}
        """
        return {'Authorization': 'Bearer ' + access_token}

    def get_refresh_token_code_from_file(self):
        """
            Get 'refresh token' code from 'refresh_token.txt'
            For request to refreshing 'access token'
        """
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            file = open(path + '/refresh_token.txt', 'r')
            return file.readlines()
        except FileNotFoundError:
            return False

    def access_token_control(self, header_bearer):
        """
            Checks whether the access token expires.
            If access token expires, returns False

            Params:
                header_bearer -- bearer header of access token
                    example -> '{Authorization: Bearer NgCXRK...MzYjw}'

        """
        url = 'https://api.spotify.com/v1/me/playlists'
        req = requests.get(url, headers = header_bearer)
        if req.status_code == 200:
            return True
        else:
            return False

    def get_song_name(self):
        """
            Gets song name that is currently playing on Spotify and returns it.
        """
        url = 'https://api.spotify.com/v1/me/player/currently-playing'
        req = requests.get(url, headers=self.authorization_header_bearer(self.access_token))
        if req.status_code == 200:
            items = req.json()
            artist = items["item"]["artists"][-1]["name"]
            track_name = items["item"]["name"]
            song = artist + " " + track_name # Eg. Rammstein Stripped
            return song
        else:
            return None

    def main(self):
        bearer_header = self.authorization_header_bearer(self.access_token)
        if self.access_token_control(bearer_header) == False: # if access token expires
            header_base64 = self.authorization_header_base64(
                self.spotify_client_id,
                self.spotify_client_secret)
            # refresh 'access token'
            self.access_token = self.refresh_access_token(
                self.refresh_token,
                header_base64)
        return self.get_song_name()
