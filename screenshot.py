import requests
import os
import json
import argparse
import time
from imgurpython import ImgurClient
from subprocess import Popen, PIPE
from pathlib import Path
###CONFIG BEGIN###
client_id = 'ce74d297d88409f' #imgur application client id
client_secret = '098e40600fe21f3a8e675a497c3b80cf4c33e844' #imgur application client secret
access_token = 'c340cbb5e2a0472bb491fda4421a13bb724a3381' #user specifc access token
refresh_token = '94db223c23714bc13fcba9e8b170d9c965605b9e' #user specifc refresh token
file_name = 'Image'
date_format = '%Y%m%d-%H%M%S'
file_loc = '~/Pictures'
###CONFIG END###


def GenerateFileName(name, dateformat):
    while True:
        try:
            dateformat = time.strftime(dateformat)
        except ValueError:
            print("ERROR: Invalid date format provided")
            dateformat = input("Please enter a valid date format: ")
        return name + '-' + dateformat + '.png'
def paste(str, p=True, c=True):
    from subprocess import Popen, PIPE

    if p:
        p = Popen(['xsel', '-pi'], stdin=PIPE)
        p.communicate(input=str)
    if c:
        p = Popen(['xsel', '-bi'], stdin=PIPE)
        p.communicate(input=str)
def InitializeImgurClient(client_id, client_secret):
    return ImgurClient(client_id, client_secret)
def InitializeImgurClient(client_id, client_secret, access_token, refresh_token):
    return ImgurClient(client_id, client_secret, access_token, refresh_token)
def UploadToImgur(target, anonymous=False):
    if anonymous == True:
        client = InitializeImgurClient(client_id, client_secret)
        upload = client.upload_from_path(target, config=None, anon=anonymous)
        return upload['link'].encode()
    elif anonymous == False:
        client = InitializeImgurClient(client_id, client_secret, access_token, refresh_token)
        upload = client.upload_from_path(target, config=None, anon=anonymous)
        return upload['link'].encode()
    else:
        print("ERROR: Anonymous parameter not boolean")
        UploadToImgur(input("Anonymous upload? (True/False)"))
def CaptureScreen(name='Image', dateformat='%Y%m%d-%H%M%S', path='~/Pictures'):
    filename = GenerateFileName(name, dateformat)
    os.system('scrot -s -d 5 ' + filename + ' -e "mv ' + filename + ' ' + path + '"')
    return str(Path.home()) + '/Pictures' + '/' + filename

def Process(upload=True, echo=True, clipboard=True):
    target = CaptureScreen(file_name, date_format, file_loc)
    if upload:
        link = UploadToImgur(target)
        if echo:
            print(link.decode('utf-8'))
        if clipboard:
            paste(link)
    else:
        if echo:
            print(target)
        if clipboard:
            paste(target.encode())

Process(True, True, True)
