from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
	path('', landing, name='landing'),
	path('soal', soal, name='soal'),
	path('hasil', hasil, name='hasil')
]