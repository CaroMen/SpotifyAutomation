import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


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

    def get_playlists(self):
        request = self.youtube.playlists().list(
            # The part parameter specifies a comma-separated list of one or more
            # playlist resource properties that the API response will include.
            part="id, snippet",
            # The maxResults parameter specifies the maximum number of items
            # that should be returned in the result set
            maxResults=40,
            mine=True  # ?
        )

        response = request.execute()

        # creates list in variable playlist of the 'id' (what youtube uses to uniquely identify the playlist),
        # the 'snippet' (what contains details about the playlist) and 'title (the title)
        playlists = [playlist(item['id'], item['snippet']['title'])
                     for item in response['items']]
