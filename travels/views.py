from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User
import requests
import json
import random


def index(request):    
    return render(request, "travels/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "travels/index.html", {"page": "login",
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "travels/index.html", { "page": "login" })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travels/index.html", {"page": "register", 
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travels/index.html", {"page": "register", 
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travels/index.html", { "page": "register" })


def getPhotos(request):
    response = requests.get("https://api.teleport.org/api/urban_areas/").json()
    cities = response.get('_links').get('ua:item')
    rand_list = random.sample(cities, 6)
    pictures = []
    for i in rand_list:
        link = i.get('href') + 'images'
        img_info = requests.get(link).json()
        img = img_info.get("photos")[0].get("image")
        pictures.append(img)
    return JsonResponse({"links": pictures, "info":rand_list }, safe=False)


def city(request):
    city = username = request.POST["city"]
    response = requests.get("https://api.teleport.org/api/cities/?search="+ str(city)).json()
    matching_cities = response.get("_embedded").get("city:search-results")
    full_name = [i.get("matching_full_name") for i in matching_cities]
    links = [i.get("_links").get("city:item").get("href") for i in matching_cities]
    res = dict(zip(full_name, links))
    ##test = requests.get(links[0].get("city:item").get("href")).json()
    ##my_area =[i.get('ua:item') for i in  links]
    ##test = [ i for i in my_area if i.get('name').lower() == city.lower() ]
    ##links = response.get('_links').get('curies')
    ##test = [ i for i in urban_area if  i.get('name') == city]
    return render(request, "travels/city.html", {"city": full_name, "links": res })