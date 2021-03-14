# -----------------------------------------------------------
# A static site generator that works with the instagram API
# in order to create a simple modern website using the images
# already uploaded on an instagram site
# (C) 2020 Greg Morton, Hawaii, USA
# Released under the Zlib license(https://opensource.org/licenses/Zlib)
# email morton.greg@gmail.com
# -----------------------------------------------------------

from flask_wtf import FlaskForm
from flask import Flask, g, render_template, redirect, url_for, flash, session, abort, request, render_template_string, send_file
from flask_bootstrap import Bootstrap
from PIL import Image
from requests import get
from pathlib import Path
from config import Config


from pprint import pprint
import io
import requests
import os
import re
import zipfile
import shutil
import instagram
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


'''
' Checks wether a session has given this app permission to access the users 
' Instagram account, if so, the user can procede with the static site generator,
' If not, they are returned to the start page and cannot procede
'''
@app.route('/authorize')
def authorize():
    try:
        auth_code = request.args.get('code')
        if auth_code is not None:
            session['auth_code'] = auth_code
    except:
        print("Auth code is None!")

    result = instagram.getAccessToken(app.config['INSTAGRAM_CLIENT_ID'], app.config['INSTAGRAM_CLIENT_SECRET'], app.config["INSTAGRAM_REDIRECT_URI"] , session['auth_code'])
    pprint(result)
    session['access_token'] = result["access_token"]
    session['instagram_id'] = result["user_id"]
    session['images'] = getImages()

    return redirect(url_for('start'))

'''
' Checks wether the user has been authorized, if so the function returns True, 
' if not the function returns false
'''
def isAuthorized():
    if session.get('auth_code') is not None:
        return True
    return False

'''
' Clears the users work on the site and returns all data back to the default page data
' The user is still logged in and can continue working on their site
'''
@app.route('/clear')
def clear():
    session["navbar"] = "NavBar"
    try:
        del session['start']
    except:
        pass
    try:
        del session['services']
    except:
        pass
    try:
        del session['about']
    except:
        pass

    return redirect(request.referrer)

'''
' Clears all session data, including the users instagram information and logs them out of the site generator
'''
@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())]

    return redirect(url_for("index"))

'''
' Takes a URL and saves the data located at the URL as a binary file. Used to download images 
' from instagram to store locally
'''
def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


'''
' Loads page data from files and returns the data as a list of strings. 
' Used in order to load the default data for  the dynamic parts of the
' site that can be modified by the user
'''
def getDefaultPageData(filename):
    text_data = list()
    base_path = str(Path(__file__).parent) + "/data/page_defaults/"

    with open(base_path+filename) as f:
        text_data = f.readlines()

    return text_data



'''
' Loads the start page, the first page the user sees and can modify upon loggin in.
'''
@app.route('/start')
def start():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    if session["navbar"] is None:
        session["navbar"] = "Navbar"
    g.navbar = session["navbar"]

    text_data = None
    
    # If the page has already been modified, get the current version of the page, if not, load the defaults
    try:
        text_data = session['start']
    except:
        text_data = getDefaultPageData("start.txt")

    return render_template('start.html', images=session['images'], site_style=session['site_style'], text_data=text_data)


'''
' Loads the about page, the 2nd page the user sees and can modify upon loggin in.
'''
@app.route('/about')
def about():
    g.navbar = session["navbar"]

    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    text_data = None
    try:
        text_data = session['about']
    except:
        text_data = getDefaultPageData("about.txt")

    return render_template('about.html', images=session['images'], text_data=text_data, site_style=session['site_style'])


'''
' Loads the services page, the third page the user sees and can modify upon loggin in.
'''
@app.route('/services')
def services():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    g.navbar = session["navbar"]
    text_data = None
    try:
        text_data = session['services']
    except:
        text_data = getDefaultPageData("services.txt")

    return render_template('services.html', images=session['images'], text_data=text_data, site_style=session['site_style'])


'''
' Returns the instagram URL of image selected with javascript.
' This function is called after a user is presented with a list of the instagram
' images on their account and makes a selection
'''
@app.route('/selectImage')
def selectImage():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    img_url = request.args.get('img_url', "0", type=str)
    return img_url


'''
' Generates a favicon from a selected instagram image
' This function is called after a user is presented with a list of instagram 
' images on their account and selects the one to use as a favicon
'''
@app.route('/set_favicon', methods=['GET', 'POST'])
def set_favicon():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    base_path = str(Path(__file__).parent) + "/data/" + str(session['instagram_id'])
    img_path = base_path + "/favicon.jpg"
    favicon_path = base_path + "/favicon.ico"

    favicon_url = request.args.get('favicon', "0", type=str)
    download(favicon_url, img_path)
    favicon_img = Image.open(img_path)
    favicon_img.save(favicon_path)


'''
' Changes the CSS style used to generate the users final site
'''
@app.route('/change_style', methods=['GET', 'POST'])
def change_style():
    session['site_style'] = "static/" + str(request.form.get("cssFile"))


'''
' Saves the changes of a modified page.
' Used whenever a user leaves a page that they have modified'
'''
@app.route('/save_page', methods=['GET', 'POST'])
def save_page():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    g.navbar = session["navbar"]

    page_id = str(request.form.get("pageID"))

    # updated: get value for key "html", encode correctly
    data = str(request.form.get("html"))
    page_data = list()
    for line in data.splitlines():
        if "data-editable" in line or "image-editable" in line:
                page_data.append(line)
                print(line)
        if "navbar-editable" in line:
                session["navbar"] = re.search('>(.*)<', line).group(1)

    session[page_id] = page_data
    if page_id == "downloadSite":
        return downloadSite()
    else:
        return redirect(url_for('start'))

'''
' Downloads the generated page as a zip file
' Used after a user has completed creating their site and is ready to download the final version'
'''
@app.route('/downloadSite', methods=['GET', 'POST'])
def downloadSite():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    base_path = str(Path(__file__).parent)
    data_path = base_path + "/data/"

    os.makedirs(data_path + str(session['instagram_id']), exist_ok=True)
    os.makedirs(data_path + str(session['instagram_id']) + "/static", exist_ok=True)

    start_data = None
    about_data = None
    services_data = None

    try:
        start_data = session['start']
    except:
        start_data = getDefaultPageData("start.txt")

    try:
        about_data = session['about']
    except:
        about_data = getDefaultPageData("about.txt")

    try:
        services_data = session['services']
    except:
        services_data = getDefaultPageData("services.txt")

    # Make directory
    start = open(data_path + str(session['instagram_id']) + "/start.html", "w")
    about_page = open(data_path + str(session['instagram_id']) + "/about.html", "w")
    services_page = open(data_path + str(session['instagram_id']) + "/services.html", "w")
    g.navbar = session["navbar"]

    start.write(render_template('file_start.html', images=session['images'], site_style=session['site_style'], text_data=start_data).encode('ascii', 'ignore').decode('ascii'))
    about_page.write(render_template('file_about.html', images=session['images'], site_style=session['site_style'], text_data=about_data).encode('ascii', 'ignore').decode('ascii'))
    services_page.write(render_template('file_services.html', images=session['images'], site_style=session['site_style'], text_data=services_data).encode('ascii', 'ignore').decode('ascii'))
    shutil.copyfile(str(app.root_path) + "/" + session['site_style'], data_path + str(session['instagram_id']) + "/" + session['site_style'])

    start.close()
    about_page.close()
    services_page.close()

    data = io.BytesIO()
    data_path = Path(str(data_path) + "/" + str(session['instagram_id']))

    with zipfile.ZipFile(data, "w") as zip_file:
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if dirs:
                    zip_file.write(os.path.join(root, file), str(session['instagram_id']) + "/" + file)
                else:
                    zip_file.write(os.path.join(root, file), str(session['instagram_id']) + "/static/" + file)

    data.seek(0)
    zip_file.close()
    return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='your_site.zip')

'''
' Returns a list of URLs for the instagram images on a users Instagram account
' Used whenever a user needs to select an image for their site
'''
@app.route('/getImages')
def getImages():
    if isAuthorized() is False:
        flash('You are not authorized to access this page, please reauthenticate your instagram account')
        return redirect("/")

    return instagram.getInstagramImages(session['access_token'])

'''
' Displays the final page the user sees after completing their site and is ready to download their 
' completed copy'
'''
@app.route('/final')
def final():
    return render_template('final.html', site_style="static/darkly.css")


'''
' The welcome page
' The first page the user sees before they login to begin creating their site.
'''
@app.route('/')
def index():
    session["navbar"] = "NavBar"
    session['site_style'] = "static/darkly.css"
    return render_template('welcome.html', site_style="static/darkly.css")



if __name__ == "__main__":
    app.run(ssl_context='adhoc')
