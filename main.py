import json
import requests
from secrets import spotify_user_id, discoverWeeklyID, newPlaylistID
from refreshToken import Refresh

class savetoPlaylist:
    def __init__(self):
        self.userId = spotify_user_id
        self.spotifyToken = ""
        self.discoverWeeklyID = discoverWeeklyID
        self.basedSongs = ""
        self.newPlaylistID = newPlaylistID

    def getSongs(self):
        print("Step 2: Find songs in discover weekly...")
        # loop through discover weekyly tracks and add to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discoverWeeklyID)

        response = requests.get(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)
        })

        response_json = response.json()
        #print(response)

        for x in response_json["items"]:
            self.basedSongs += (x["track"]["uri"] + ",")
        #remove the extra comma at the end of the string
        self.basedSongs = self.basedSongs[:-1]
        print(self.basedSongs)
        self.putSongsOnPLaylist()


    def putSongsOnPLaylist(self):
        print("Step 3: Adding songs to new playlist...")
        # add all the songs to the playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.newPlaylistID,self.basedSongs)
        response = requests.post(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)
        })
        print(response.json())


    def callRefresh(self):
        print("Step 1: Refreshing Spotify token")
        refreshCall = Refresh()
        self.spotifyToken = refreshCall.refresh()
        self.getSongs()

run = savetoPlaylist()
run.callRefresh()
