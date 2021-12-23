import json
import requests
from secrets import spotify_token, spotify_user_id, discoverWeeklyID

class savetoPlaylist:
    def __init__(self):
        self.userId = spotify_user_id
        self.spotifyToken = spotify_token
        self.discoverWeeklyID = discoverWeeklyID

    def getSongs():
        # loop through discover weekyly tracks and add to list
        # playlist uri = spotify:playlist:37i9dQZEVXcS5kDYDE5AFV
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discoverWeeklyID)

        response = requests.get(query,headers={
            "Contenty-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })

        response_json = response.json
        print(response)

run = savetoPlaylist()
run.getSongs