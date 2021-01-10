import requests
import base64
import datetime
from urllib.parse import urlencode
import json

CLIENT_ID = "5604f608bd3d4d4eb45d99673914efdf"
CLIENT_SECRET = "031818f773294a03b94752980da7bebf"
CODE = 'AQByCjD7HN8mTRp11B3cfo1UDgo5vUTct0owsDHObUT4-jQNlAdX-AqfifYfDDeq36gwP4Fka-1Qyj5p3VxEJVWKZfy6g9-WWZ7IpZTHQXOuc8x2SL2_jgJzGZbqaQZ9cqbmxTmJPCCyx7_8mSMEzg96rjJKkiOwTeKoUVts4WHsaesUA-30U0pfFoiFNcQpChM1zd2SNjWsOg'
data = {
'access_token': 'BQDMCoMDtQh8jdvTxlPuPGXd8IJHooLKu5ZQ6rDW_IZDbE4KXgXk7skWjKe4b8cezzWMLfeP8qBBsvVCx9xDXVKs6dY5DokutLDwQM2_DOfcVvZ0dLS4nlTFgfUyrwr-JspGKN-a7Ik9DCKRWEBCjIpIjMPXTYPuS_0ONZe0yFtjcAc',
'token_type': 'Bearer',
'expires_in': 3600,
'refresh_token': 'AQBd3UK-Wd-DsgqWtrx3AZ0RIn4KJrVxJb2EaDAX0rmPslrBQVAoF_YOuONZk9HgVegP_8WyTEIXeVzRETOGQUDs8lrG_3VeRAaMfhkVd9gRMLv49XrnOVWKCJquzN7bK8k',
'scope': 'playlist-read-private'
}

playlist_id = '0VnxiT9E4PtRxLf68Pmrod'
playlist = []


class SpotifyAPI(object):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    auth_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret


    def get_client_credentials(self):
        '''
        return a base64 encoded str 
        '''
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization" : f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return{
            "grant_type" : "authorization_code",
            'code' : CODE,
            'redirect_uri' : 'http://localhost:8888/callback/'
        }

    def get_auth(self):
        auth_url = self.auth_url
        data = urlencode({
            'client_id' : self.client_id,
            'response_type' : 'code',
            'redirect_uri' : 'http://localhost:8888/callback/',
            'scope' : 'playlist-read-private',
            'show_dialog' : 'false'
             })
        lookup_url = f"{auth_url}?{data}"
        print(lookup_url)
        # r = requests.get(lookup_url)

    def get_Acces(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        print(data)
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def refrech_token(self):
        headers = self.get_token_headers()
        data = {
            'grant_type' : 'refresh_token',
            'refresh_token' : self.refresh_token
        }
        endpoint = 'https://accounts.spotify.com/api/token'
        r = requests.post(endpoint, data = data, headers=headers)
        # print(r.json())
        self.access_token = r.json()['access_token']

    # def search(self):
    #     access_token = self.access_token
    #     headers = {
    #         "Authorization" : f"Bearer {access_token}"
    #     }
    #     endpoint = "https://api.spotify.com/v1/search"
    #     data = urlencode({"q": "favourites", "type": "playlist"})
    #     print(data)
    #     lookup_url = f"{endpoint}?{data}"
    #     r = requests.get(lookup_url, headers = headers)
    #     print(r.json())
    #     return

    def search_playlist(self, playlist_id):
        access_token = self.access_token
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        songs = []
        count = 0
        while count < 3:
            data = urlencode({'offset': count*100})
            endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?{data}"
            r = requests.get(endpoint, headers=headers)
            results = r.json()['items']
            for song in results:
                artists = [artist['name'] for artist in song['track']['artists']]
                result = {'song_name': song['track']['name'],
                          'artist_name': ", ".join(artists)
                          }
                songs.append(result)
            count +=1

        with open('./songs.json', 'w') as f:
            json.dump(songs, f, indent=4)



    # def get_my_playlists(self):
    #     access_token = self.access_token
    #     headers = {
    #         "Authorization" : f"Bearer {access_token}"
    #     }
    #     endpoint = f"https://api.spotify.com/v1/me/playlists"
    #     r = requests.get(endpoint, headers = headers)


if __name__ == '__main__':
    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    spotify.refrech_token()
    spotify.search_playlist(playlist_id)
