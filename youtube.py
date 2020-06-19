import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl


class playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class YouTubeCL(object):
    def __init__(self, creds_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            creds_location, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube = youtube

    # Step One: Get the playlists from user
    def get_playlists(self):
        request = self.youtube.playlists().list(
            # The part parameter specifies a comma-separated list of one or more
            # playlist resource properties that the API response will include.
            part="id, snippet",
            # The maxResults parameter specifies the maximum number of items
            # that should be returned in the result set
            maxResults=40,
            mine=True
        )

        response = request.execute()

        # creates list in variable playlist of the 'id' (what youtube uses to uniquely identify the playlist),
        # the 'snippet' (what contains details about the playlist) and 'title (the title)
        playlists = [playlist(item['id'], item['snippet']['title'])
                     for item in response['items']]

        return playlists

    # Step Two: Get the names of artists and tracks from playlist
    def get_vids(self, playlist_id):
        songs = []
        video_request = self.youtube.playlistItems().list(
            playlistID=playlist_id,
            part="id, snippet",
            maxResults=40
        )

        response = video_request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist = self.get_vids(video_id)
            track = self.get_vids(video_id)

            if artist and track:
                songs.append(Song(artist, track))

            return songs

    def get_music(self, video_id):
        pass
