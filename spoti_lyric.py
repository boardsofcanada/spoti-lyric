# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

from tkinter import *
from song_name import SongName
from search_find_lyric import lyric_main


class SpotiLyric:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        """
            Params:
                client_id -- client id of your API which register to Spotify.
                client_secret -- client secret id of your API which register to Spotify.
                redirect_uri -- 'redirect uri' which you have been entered when you register your API.
                scope -- a space-separated list of scopes.

            Example use of:
                - SpotiLyric()
        """
        self.SPOTIFY_CLIENT_ID = client_id
        self.SPOTIFY_CLIENT_SECRET = client_secret
        self.SPOTIFY_REDIRECT_URI= redirect_uri
        self.SPOTIFY_SCOPE = scope
        self.temp_song_name = ' ' # temporary variable for catch to changing songs.
        #
        self.s = SongName(self.SPOTIFY_CLIENT_ID,
                    self.SPOTIFY_CLIENT_SECRET)
        # tkinter
        self.top = Tk()
        self.top.attributes('-topmost', 1)
        self.scroll = Scrollbar(self.top)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.height = self.top.winfo_screenheight()
        self.top.geometry("480x{}".format(self.height))

        # tkinter text settings
        self.text = Text(self.top, font=('Helvetica', 12))
        self.text.tag_configure('bold', font=('Helvetica',16, 'bold'))
        self.text.tag_configure('tiny', font=('Helvetica',10, 'italic'))
        self.text['bg'] = '#FFF'
        self.text['fg'] = '#222'
        # main program loop
        self.run()
        self.top.mainloop()

    def add_lyric_to_tk(self, song_name, lyric, url = ' '):
        """
            Processes of Tkinter Text()
            Inserts the lyrics, adds names of tracks to the title bar...
        """
        self.top.title(song_name)
        self.text.delete("1.0",END) # when song change, delete previous lyric
        self.text.insert(INSERT, song_name,'bold')
        self.text.insert(INSERT, "\n\n\n")
        self.text.insert(INSERT, lyric)
        self.text.insert(INSERT, "\n\n----\n")
        self.text.insert(INSERT, url, 'tiny')
        self.text.pack(expand=True, fill=BOTH)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)

    def get_song_name(self):
        """
            Returns the song name that is currently playing on Spotify
        """
        return self.s.main()

    def get_lyric(self, song_name):
        """
            Returns the lyric of song which given as parameter.
        """
        return lyric_main(song_name)

    def run(self):
        song = self.get_song_name()
        if self.temp_song_name != song and song != None:
            print("Song changed...")
            # if program runs first time or playing song changes
            lyric = self.get_lyric(song)
            self.temp_song_name = song
            self.add_lyric_to_tk(song, lyric[0], lyric[1])
        self.top.after(10000,self.run)
