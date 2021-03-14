# -----------------------------------------------------------
# A static site generator that works with the instagram API
# in order to create a simple modern website using the images
# already uploaded on an instagram site
# (C) 2020 Greg Morton, Hawaii, USA
# Released under the Zlib license(https://opensource.org/licenses/Zlib)
# email morton.greg@gmail.com
# -----------------------------------------------------------

import json
import requests
from requests import get
from pprint import pprint
'''
' Takes in the info for the instagram app and returns the access token
' Used whenever the application needs a new access to access the Instagram API'
'''
def getAccessToken(client_id, client_secret, redirect_uri, auth_code):
    files = {
        'client_id': (None, client_id),
        'client_secret': (None, client_secret),
        'grant_type': (None, 'authorization_code'),
        'redirect_uri': (None, redirect_uri),
        'code': (None, auth_code),
    }

    response = requests.post('https://api.instagram.com/oauth/access_token', files=files)
    return json.loads(response.text)

'''
' Takes in the access token for instagram and outputs a list of images on a users account
'''
def getInstagramImages(access_token):
    params = (
        ('access_token', access_token),
    )

    response = requests.get('https://graph.instagram.com/me/media', params=params)
    pprint(response.text)   
    images = json.loads(response.text)
    image_data = list()
    for image in images['data']:
        image = getInstagramImage(image['id'], access_token)['media_url']
        image_data.append(image)

    return image_data

'''
' Takes in an access token for instagram and a specific image ID for a users instagram account
' and returns an image URL.
' Used whenever a specific image is needed from a users account'
'''
def getInstagramImage(image_id, access_token):
    params = (('fields', 'id,media_type,media_url,timestamp'),
              ('access_token', access_token))
    response = requests.get('https://graph.instagram.com/' + image_id + '/', params=params)
    return json.loads(response.text)
