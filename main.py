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
        self.songsToDelete = []
        self.newPlaylistID = newPlaylistID
        self.deleteDict = {}
        self.whoa = ''

    def getSongs(self):
        print("Step 4: Find songs in this week's discover weekly...")
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
        #print(self.basedSongs)
        self.putSongsOnPLaylist()

    def getSongsToDelete(self):
        print("Step 2: Getting Songs from Last week's discover weekly...")
        # loop through discover weekyly tracks and add to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(newPlaylistID)

        response = requests.get(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)
        })

        response_json = response.json()


        for x in response_json["items"]:
            #self.songsToDelete += (x["track"]["uri"] + ",")

            dict = {"uri": (x["track"]["uri"])}
            self.songsToDelete.append(dict)

        self.deleteLastWeek()


    def putSongsOnPLaylist(self):
        print("Step 5: Adding songs to new playlist...")
        # add all the songs to the playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.newPlaylistID,self.basedSongs)
        response = requests.post(query,headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)
        })
        #print(response.json())


    def callRefresh(self):
        print("Step 1: Refreshing Spotify token...")
        refreshCall = Refresh()
        self.spotifyToken = refreshCall.refresh()
        self.getSongsToDelete()

    def deleteLastWeek(self):
        print("Step 3: Deleting song from last week...")


        self.deleteDict = {"tracks":self.songsToDelete}
        finalDump = json.dumps(self.deleteDict)


        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.newPlaylistID)
        response = requests.delete(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)},
            data=finalDump)
        response_json = response.json()

        self.getSongs()


run = savetoPlaylist()
run.callRefresh()
print("Successfully created new discover weekly playlist")
