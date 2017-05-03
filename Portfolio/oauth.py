import json
import os
from django.core.files import File

import httplib2
import oauth2client
import urllib.request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from oauth2client import client
from django.shortcuts import redirect

from django.shortcuts import render
from Portfolio import views
from Portfolio.models import GoogleAccessToken, Commentor


# Get
def get_google_credential(request):
    client_key = json.load(open('static/Portfolio/json/google.json'))
    flow = client.OAuth2WebServerFlow(
        client_id=client_key['web']['client_id'],
        client_secret=client_key['web']['client_secret'],
        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=request.build_absolute_uri(reverse('finish_google_auth'))
    )
    return flow


def start_google_auth(request):
    redirect_uri = request.GET.get('redirect_uri')
    return HttpResponseRedirect(get_google_credential(request).step1_get_authorize_url())


def finish_google_auth(request):
    # redirect_uri = request.get_context_data('redirect_uri')

    # Get credential
    flow = get_google_credential(request)
    auth_code = request.GET.get('code')
    credential = flow.step2_exchange(auth_code)
    credential_json = json.loads(credential.to_json())

    # Save account info into DB.
    save_account_info(credential_json)

    # Fill in refresh_token value of json file if it's empty.
    if credential_json['refresh_token'] is None:
        refresh_token = GoogleAccessToken.objects.values_list('refresh_token').filter(email=credential_json['id_token']['email']).first()[0]
        if refresh_token is not None:
            credential_json['refresh_token'] = refresh_token

    # Save credential as a json file and session variable
    f = open('static/Portfolio/json/'+credential_json['id_token']['email']+'.json', 'w')
    f.write(json.dumps(credential_json))
    f.close()
    if credential_json['refresh_token'] is not None:
        access_token = GoogleAccessToken.objects.filter(email=credential_json['id_token']['email'])
        if len(access_token) > 0:
            access_token.update(refresh_token = credential_json['refresh_token'])
        else:
            token = GoogleAccessToken(email=credential_json['id_token']['email'], refresh_token=credential_json['refresh_token'])
            token.save()

    request.session['email'] = credential_json['id_token']['email']

    try:
        return redirect(request.META['HTTP_REFERER'])
    except KeyError:
        return redirect(reverse('intro'))


def refresh_credential(request, credential_json):
    if credential_json['refresh_token'] is None:
        print("fuck")
        credential_json['refresh_token'] = GoogleAccessToken.objects.values_list('refresh_token').filter(email=credential_json['id_token']['email'])[0]
    credential = oauth2client.client.Credentials.new_from_json(json.dumps(credential_json))
    http = credential.authorize(httplib2.Http())
    try:
        credential.refresh(http)
        print("??????????????/")
    except Exception:
        print("???")
        start_google_auth(request)


def logout(request):
    try:
        request.session.pop('email')
    except KeyError:
        pass
    return redirect(request.META['HTTP_REFERER'])


def save_account_info(credential_json):
    email = credential_json['id_token']['email']

    # Save picture in filesystem if image is available
    save_image_from_url(
        './static/Portfolio/img/comment/commentor/' + credential_json['id_token']['email'] + '.png',
        credential_json['id_token']['picture']
    )

    # Save account information into DB
    if not Commentor.objects.filter(email=email):
        commentor = Commentor(
            email=email,
            name=credential_json['id_token']['name'],
            picture='static/Portfolio/img/comment/commentor/' + credential_json['id_token']['email'] + '.png'
        )
        commentor.save()


def save_image_from_url(file_name, url):
    profile_image = urllib.request.urlopen(url)

    if profile_image.getcode() is 200:
        file_to_save = open(file_name, "wb")
        while True:
            buf = profile_image.read(4096)
            if len(buf) == 0:
                break
            file_to_save.write(buf)
        file_to_save.close()

    profile_image.close()


