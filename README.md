# spoti-lyric
Displays on GUI Window the lyrics of the song that is currently playing on Spotify.

![example](https://i.imgur.com/KQPfTED.png)


# Usage

* Create an app at https://developer.spotify.com/dashboard/applications, enter "http://localhost/" for the **Redirect URIs**


* Change the following lines in **config.py** according to your created spotify app

  ```
  SPOTIFY_CLIENT_ID = 'client id of your app (from developer.spotify.com)'
  SPOTIFY_CLIENT_SECRET = 'client secret of your app (from developer.spotify.com)'
  SPOTIFY_REDIRECT_URI= 'http://localhost'
  ```

* Run  ```run.py ```

* The program will ask a url for authorize when first run. You just need to copy url from opened web browser and paste it to pgoram.*(After allow your developer account on opened browser.)* **Example** url of you need to paste --> http://localhost/?code=...,

* After paste url, the program creates **refresh_token.txt** and writes refresh token code to the file. The program needs this file to run.


# How Work?
* Your Spotify application authorizes.
* Gets song name that is currently playing on Spotify.
* Searches the song name on Google. 
* If the song lyric found, - after some web scraping - the lyric displays on GUI.


# Adds 
 * Only searches within the sites given below. (New sites will be added to increase the probability of finding)
```
  - Metrolyrics.com
  - Genius.com
  - Azlyrics.com
```
* When token expired, refreshing automatically.


# Requirements (tested versions)
**pip install -r requirements.txt**
  ```
Python 3.6.5
Requests 2.11.1
Beautifulsoup4 4.6.0
  ```
