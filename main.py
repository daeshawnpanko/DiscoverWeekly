import json
import requests
from secrets import spotify_token, spotify_user_id, discoverWeeklyID, newPlaylistID

class savetoPlaylist:
    def __init__(self):
        self.userId = spotify_user_id
        self.spotifyToken = spotify_token
        self.discoverWeeklyID = discoverWeeklyID
        self.basedSongs = ""
        self.newPlaylistID = newPlaylistID

    def getSongs(self):
        print("Step 1: Find songs in discover weekly...")
        # loop through discover weekyly tracks and add to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discoverWeeklyID)

        response = requests.get(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
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
        print("Step 2: Adding songs to new playlist...")
        # add all the songs to the playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.newPlaylistID,self.basedSongs)
        response = requests.post(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })
        print(response.json())


run = savetoPlaylist()
run.getSongs()
