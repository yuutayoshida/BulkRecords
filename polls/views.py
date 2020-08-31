from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Save
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.http import HttpResponse
import tmdbsimple as tmdb
import spotipy
import sys
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import os
import urllib.parse
RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = '1082042096723903381'
tmdb.API_KEY = '1c8dee5cdaf6294a7c742f5821f4108d'
client_id = 'e6cbdc037d6747dd9988ba6af9939a1c'
client_secret = 'b07e4f608b71411cb089d1d081aaf7ff'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.

def search(request):
  if 'movie_query' in request.GET:
    keyword = str(request.GET.get('movie_query', ''))
    if keyword != '':
      search = tmdb.Search()
      response = search.movie(query=keyword)
      responses = search.results
      for i in range(len(responses)):
        responses[i]['category'] = 1

    else:
      responses = {}
    return render(request, 'polls/top.html',{'responses':responses})
  elif 'music_query' in request.GET:
    keyword = str(request.GET.get('music_query',''))
    if keyword != '':
      response = sp.search(q=keyword, limit=50, offset=10, type='album', market=None)
      responses = []
      for album in response['albums']['items']:
        result = {'title':album['name'],'release_date':album['release_date'],'id':album['id']}
        for artist in album['artists']:
          result['artist_name'] = artist['name']
        images = album['images'][0]
        result['image'] = images['url']
        result['category'] = 2
        responses.append(result)
    else:
      responses = {}
    return render(request, 'polls/top.html',{'responses':responses})
  elif 'book_query' in request.GET:
    keyword = str(request.GET.get('book_query',''))
    keyword_quote = urllib.parse.quote(keyword)
    if keyword != '':
      response = requests.get('{}?format=json&title={}&booksGenreId=001004008&hits=10&applicationId={}'.format(RAKUTEN_BOOKS_API_URL,keyword_quote,RAKUTEN_APP_ID))
      responses=[]
      for i in range(int(response.json()["hits"])):
          title = response.json()["Items"][i]["Item"]['title']
          author = response.json()["Items"][i]["Item"]['author']
          image = response.json()["Items"][i]["Item"]['mediumImageUrl']
          id = response.json()["Items"][i]["Item"]['isbn']
          result = {'title':title,'author':author,'image':image,'id':id}
          result['category'] = 3
          responses.append(result)
    else:
      responses = {}
    return render(request, 'polls/top.html',{'responses':responses})

  else:
      responses = Save.objects.all().order_by('-post_date')[:14]
      return render(request, 'polls/top.html',{'responses':responses})

@login_required
def detail(request, category=None, id=None):
  #category 1=movie 2=music 3=book
  user = request.user
  saved_user = Save.objects.filter(post_id = id)
  saved_or = {}
  save_item = Save.objects.filter(post_id=id,user=user)
  if save_item.count() > 0:
    saved_or['saved'] = 0
  else:
    saved_or['saved'] = 1

  if category == 1:
    movie = tmdb.Movies(id)
    responses = movie.info()
    responses['category'] = category
    responses['category_name'] = 'Movie'
    crew = movie.credits()['crew'][0]
    author = crew['name']
    trailers = list(filter(lambda v: v['type'] == 'Trailer' or v['type'] == 'Teaser' , movie.videos()['results']))
    trailer = trailers[0]
    return render(request, 'polls/detail.html',{'responses':responses,'trailer':trailer,'author':author,'saved_or':saved_or,'saved_user':saved_user})

  elif category == 2:
    responses = sp.album('spotify:album:'+id)
    responses['category'] = category
    responses['category_name'] = 'Music'
    responses['image'] = responses['images'][0]['url']
    artist = {}
    for i in responses['artists']:
      artist['artist_name'] = i['name']
      artist['artist_id'] = i['id']
      
    tracks = []
    for track in responses['tracks']['items']:
      hoge = {}
      hoge['track_name'] = track['name']
      external_urls = track['external_urls']
      hoge['track_url'] = external_urls['spotify']
      tracks.append(hoge)
    return render(request, 'polls/detail.html',{'responses':responses,'artist':artist,'tracks':tracks,'saved_or':saved_or,'saved_user':saved_user})
  elif category == 3:
    detail_id = int(id)
    response = requests.get('{}?format=json&isbn={}&applicationId={}'.format(RAKUTEN_BOOKS_API_URL,detail_id,RAKUTEN_APP_ID))    
    responses = []
    for i in range(int(response.json()["hits"])):
        title = response.json()["Items"][i]["Item"]['title']
        author = response.json()["Items"][i]["Item"]['author']
        image = response.json()["Items"][i]["Item"]['mediumImageUrl']
        release_date = response.json()["Items"][i]["Item"]['salesDate']
        caption = response.json()["Items"][i]["Item"]['itemCaption']
        responses = {'title':title,'id':id,'author':author,'image':image,'release_date':release_date,'caption':caption,'category':category,'category_name':'Book'}
        return render(request, 'polls/detail.html',{'responses':responses,'saved_or':saved_or,'saved_user':saved_user})
    #book=9784101355511,movie=149,music=5ng5dilD1OOQkeON0kpaxd
    
def users_detail(request, pk):
  user = get_object_or_404(User, pk=pk)
  saved = user.save_set.all().order_by('-post_date')
  return render(request, 'polls/users_detail.html',{'user':user,'saved':saved})

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      input_username = form.cleaned_data['username']
      input_password = form.cleaned_data['password1']
      new_user = authenticate(username=input_username,password=input_password)
      if new_user is not None:
        login(request, new_user)
        return redirect('polls:users_detail', pk=new_user.pk)
  else:
    form = UserCreationForm()
  return render(request, 'polls/signup.html',{'form':form})

@login_required
def save(request, category=None, id=None):
  user = request.user
  save_item = Save.objects.filter(post_id=id,user=user)
  if save_item.count() > 0:
    save_item.delete()
    return redirect('polls:users_detail', pk=request.user.pk)
  else:  
    if category == 1:
      movie = tmdb.Movies(id)
      responses = movie.info()
      title = responses['title']
      img_url = responses['poster_path']
      crew = movie.credits()['crew'][0]
      author = crew['name']
      t = Save(title = title,post_id = id,img_url = 'http://image.tmdb.org/t/p/w185/'+img_url,category = 1,author = author,user = request.user)
      t.save()
      return redirect('polls:users_detail', pk=request.user.pk)

    elif category == 2:
      responses = sp.album('spotify:album:'+id)
      artist = {}
      title = responses['name']
      img_url = responses['images'][0]['url']
      artist = {}
      for i in responses['artists']:
        artist['artist_name'] = i['name']
      author = artist['artist_name']
      t = Save(title = title,post_id = id,img_url = img_url,category = 2,author = author,user = request.user)
      t.save()
      return redirect('polls:users_detail', pk=request.user.pk)

    elif category == 3:
      detail_id = int(id)
      response = requests.get('{}?format=json&isbn={}&applicationId={}'.format(RAKUTEN_BOOKS_API_URL,detail_id,RAKUTEN_APP_ID))    
      for i in range(int(response.json()["hits"])):
          title = response.json()["Items"][i]["Item"]['title']
          author = response.json()["Items"][i]["Item"]['author']
          img_url = response.json()["Items"][i]["Item"]['mediumImageUrl']
          t = Save(title = title,post_id = id,img_url = img_url,category = 3,author = author,user = request.user)
          t.save()
          return redirect('polls:users_detail', pk=request.user.pk)


