from django.conf.urls import url
from django.urls import path
from .views import *

app_name = 'app'
urlpatterns = [
	path('', landing, name='landing'),
	path('game', game, name='game'),
	path('soal', soal, name='soal'),
	path('hasil', hasil, name='hasil'),
]