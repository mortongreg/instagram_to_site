# instagram_to_site
A rapid static site generator that interacts with a users Instagram account and enables them to quickly walk them through creating a website using data from their instagram account. Backend is written in Python and Flask and the frontend is written in HTML/JS/CSS


## Setup

Run the following commands to install:
git clone https://github.com/mortongreg/mortongreg.github.io
pip install -r requirements.txt
export FLASK_APP=main.py

You will also need to create an Instagram application and copy related Instagram application information to the config.py file like so:

SECRET_KEY = 'SAMPLE_SECRET_KEY'

SITE_NAME = "https://sample_url.com"

INSTAGRAM_CLIENT_ID = "sample_client_id"

INSTAGRAM_CLIENT_SECRET = "sample_client_secret"

INSTAGRAM_REDIRECT_URI = "https://sample_url.com/authorize"


Once the above steps are finished you can run the application locally by the following command:
flask run



## Example

If you would like to see what the application looks like when it has been setup you can view the video below:
https://www.youtube.com/watch?v=zj6xxT04HPQ
