import requests


class DeezerService():
    @classmethod
    def search_list(self, query):
        r = requests.get('https://api.deezer.com/search?q=' + str(query))
        trackslist = r.json()['data']
        return trackslist

    @classmethod
    def search_artist(self, query):
        r = requests.get('https://api.deezer.com/search/artist?q=' + str(query))
        artists_list = r.json()['data']
        return artists_list

    @classmethod
    def verify_artist(self, track_list, allowed_artists):
        filtered_list = []
        for track in track_list:
            if track['artist']['id'] in allowed_artists:
                filtered_list.append(track)
        return filtered_list
