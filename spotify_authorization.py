# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import base64
import requests
import urllib
import webbrowser
import os

class SpotifyAuthorization:
    """
        This class authorizes your application.
        After authorize, 'refresh token' code writes to 'refresh_token.txt' for refreshing 'access token'

        Example use of:
            - a = SpotifyAuthorization(client_id, client_secret, redirect_uri, scope)
            - a.main()
    """
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        """
            Params:
                client_id -- client id of your API which register to Spotify.
                client_secret -- client secret id of your API which register to Spotify.
                redirect_uri -- 'redirect uri' which you have been entered when you register your API.
                scope -- a space-separated list of scopes.
        """
        self.spotify_client_id = client_id
        self.spotify_client_secret = client_secret
        self.spotify_redirect_uri = redirect_uri
        self.spotify_scope = scope

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

    def request_authorization(self, client_id, redirect_uri, scope):
        """
            Sends a authorization request to the Spotify Accounts service.

            Params:
                client_id -- client id of your API which register to Spotify.
                redirect_uri -- 'redirect uri' which you have been entered when you register your API.
                scope -- a space-separated list of scopes.
        """
        url = 'https://accounts.spotify.com/authorize/?'
        query_params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': scope
            }
        url = url + urllib.parse.urlencode(query_params)
        req = requests.get(url)
        webbrowser.open(req.url)

    def request_access_token(self, auth_code, redirect_uri, header_base64):
        """
            Requests the 'access token' but for this program only retrieves 'refresh token'

            Params:
                auth_code -- authorization code.
                redirect_uri -- 'redirect uri' which you have been entered when you register your API.
                header_base64 -- base 64 encoded string that contains the client ID and client secret key.

            Returns the 'refresh token'
        """
        url = 'https://accounts.spotify.com/api/token'
        body_params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri
            }
        req = requests.post(url, data=body_params, headers=header_base64)
        if req.status_code == 200:
            refresh_token = req.json()['refresh_token']
            return req.json()['refresh_token']
        else:
            return None

    def file_write(self, refresh_token):
        """
            Writes 'refresh token' to the file.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        writer = open(path + '/refresh_token.txt', 'w')
        writer.write(refresh_token)
        print("'Refresh token code' written to file")
        writer.close()

    def main(self):
        # makes authorization base64 header.
        header_base64 = self.authorization_header_base64(
            self.spotify_client_id,
            self.spotify_client_secret)
        # sends authorization request.
        self.request_authorization(
            self.spotify_client_id,
            self.spotify_redirect_uri,
            self.spotify_scope)
        # takes authorization url from user by 'input' and split the url.
        auth_code = input('Please paste url: (Ex. http://localhost/?code=AQB.....) \n')
        if '#_=_' in auth_code: # if url ends with '#_=_'
            auth_code =  auth_code.split('#')[0]
        auth_code = auth_code.split('?code=')[-1]
        # requests 'refresh token'
        refresh_token = self.request_access_token(
            auth_code,
            self.spotify_redirect_uri,
            header_base64)
        # writes 'refresh token' to file.
        self.file_write(refresh_token)
        return True
