
# Youtube Data API v3
# Step 1: https://console.developers.google.com/apis
# Step 2: Create API key and copy
# Step 3: https://console.developers.google.com/apis/library/youtube.googleapis.com
# Step 4: Enable


# PLAYLIST ITEM: INSERT
#'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key=[YOUR_API_KEY]'
'''
POST 
EXAMPLE
{
  "snippet": {
    "playlistId": "PLDeWbVJ2hh4rhHm6mahVY0PbYzSG35RzQ",
    "resourceId": {
      "kind": "youtube#video",
      "videoId": "qQxosDgZkrA"
    }
  }
}
'''


# PLAYLIST ITEM: LIST
#'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken=CDIQAA&playlistId=PLDeWbVJ2hh4otmPcfmKXq0LQU98HnrXbV&key=[YOUR_API_KEY]'
'''
GET
NOTE: pageToken parameter is found in nextPageToken or prevPageToken response. Remove pageToken if first page
'''

# PLAYLIST: DELETE
#'https://www.googleapis.com/youtube/v3/playlists?id=PLDeWbVJ2hh4rhHm6mahVY0PbYzSG35RzQ&key=[YOUR_API_KEY]'
'''
DELETE
'''

# PLAYLIST: INSERT
#'https://www.googleapis.com/youtube/v3/playlists?part=snippet&key=[YOUR_API_KEY]'
'''
POST
{
  "snippet": {
    "title": "test"
  }
}
'''

"""
1:(PLAYLIST ITEM: LIST) get all videoId from original playlist (loop)
2:(PLAYLIST: INSERT) create temporary playlist
3:(PLAYLIST ITEM: INSERT) insert all videoId from original playlist to temporary playlist
4:[OPTIONAL](PLAYLIST: DELETE) delete temp playlist
"""

#SAMPLE PLAYLIST URL
#https://www.youtube.com/playlist?list=PLDeWbVJ2hh4otmPcfmKXq0LQU98HnrXbV

# ===========================================================
# IMPORTS
# ===========================================================
import requests
import uuid
from random import shuffle

# ===========================================================
# ARGUMENTS
# ===========================================================
API_KEY = '<<ADD_API_KEY>>'

ORIG_PLAYLIST_ID = '<<ADD_PLAYLIST_ID>>'

# ===========================================================
# CONSTANTS
# ===========================================================
YT_DATA_API_URL = 'https://www.googleapis.com/youtube/v3/playlistItems?'

# ===========================================================
# FUNCTIONS
# ===========================================================
def request_original_playlist(pageToken=None):
  tokenString = ''
  if type(pageToken) is str:
    tokenString = '&pageToken=' + pageToken

  origPlaylistRequest = requests.get(YT_DATA_API_URL+'part=snippet&maxResults=50'+tokenString+'&playlistId='+ORIG_PLAYLIST_ID+'&key='+API_KEY)

  if origPlaylistRequest.status_code // 100 != 2:
    print('ERROR: '+str(origPlaylistRequest.status_code))
    exit()

  origPlaylistDict = origPlaylistRequest.json()

  return origPlaylistDict['items'], origPlaylistDict.get('nextPageToken', None)

# ===========================================================
# VARIABLES
# ===========================================================
nextPageToken = True
resourceList = []



# ===========================================================
# MAIN
# ===========================================================
if __name__ == "__main__":

  while nextPageToken:
    origItems, nextPageToken = request_original_playlist(nextPageToken)
    for itm in origItems:
      resourceList.append(itm['snippet']['resourceId'])

  resourceList = [i for i in resourceList]
  shuffle(resourceList)

  # Create Temp playlist
  uniqueId = str(uuid.uuid4())[9:13]

  playlistData = {
    "snippet": {
      "title": "YT_PLAYLIST_RANDOMIZER_"+uniqueId
    }
  }

  r = requests.post(YT_DATA_API_URL+'part=snippet&key='+API_KEY, data=playlistData, headers=header)
  from pprint import pprint
  pprint(r.json())






