"""Portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Portfolio import views, oauth

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.intro, name="intro"),
    url(r'^works/?$', views.works, name="works"),
    url(r'^interests/$', views.interests, name="interests"),
    url(r'^notes/$', views.notes, name="notes"),
    url(r'^guestbook/$', views.guestbook, name="guestbook"),

    url(r'^sesame/$', views.login, name="login"),
    url(r'^emases/$', views.logout, name="logout"),
    url(r'^write-note/$', views.notes, name="write_note"),

    url(r'^start-google-auth/', oauth.start_google_auth, name="start_google_auth"),
    url(r'^finish-google-auth/', oauth.finish_google_auth, name="finish_google_auth"),
    url(r'^logout/', oauth.logout, name="logout"),
]
