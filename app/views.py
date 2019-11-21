from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
#import requests

# Create your views here.

treeA = None

class Node():
	def __init__(self, name, value):
		self.name =  name
		self.childs = []
		self.value = value or 1

	def add_child(self, new_node):
		self.childs.append(new_node)


def createTree():
	rootA = Node("a", 1)
	rootB = Node("b", 1)
	rootC = Node("c", 1)


	rootA.add_child(Node("q1", 0.2))
	rootA.add_child(Node("q1", 0.5))
	rootA.add_child(Node("q1", 0.7))
	rootA.add_child(Node("q1", 0.9))


	for node in rootA.childs:
		node.add_child(Node("q2", 0.2))
		node.add_child(Node("q2", 0.4))
		node.add_child(Node("q2", 0.72))
		node.add_child(Node("q2", 0.89))


	for q1 in rootA.childs:
		for q2 in q1.childs:
			node.add_child(Node("q3", 0.2))
			node.add_child(Node("q3", 0.4))
			node.add_child(Node("q3", 0.72))
			node.add_child(Node("q3", 0.82))

	for q1 in rootA.childs:
		for q2 in q1.childs:
			for q3 in q2.childs:
				node.add_child(Node("q4", 0.2))
				node.add_child(Node("q4", 0.4))
				node.add_child(Node("q4", 0.72))
				node.add_child(Node("q4", 0.82))

	rootB.add_child(Node("q1", 0.2))
	rootB.add_child(Node("q1", 0.5))
	rootB.add_child(Node("q1", 0.7))
	rootB.add_child(Node("q1", 0.9))


	for node in rootB.childs:
		node.add_child(Node("q2", 0.2))
		node.add_child(Node("q2", 0.4))
		node.add_child(Node("q2", 0.72))
		node.add_child(Node("q2", 0.89))


	for q1 in rootB.childs:
		for q2 in q1.childs:
			node.add_child(Node("q3", 0.2))
			node.add_child(Node("q3", 0.4))
			node.add_child(Node("q3", 0.72))
			node.add_child(Node("q3", 0.82))

	for q1 in rootB.childs:
		for q2 in q1.childs:
			for q3 in q2.childs:
				node.add_child(Node("q4", 0.2))
				node.add_child(Node("q4", 0.4))
				node.add_child(Node("q4", 0.72))
				node.add_child(Node("q4", 0.82))

	rootC.add_child(Node("q1", 0.2))
	rootC.add_child(Node("q1", 0.5))
	rootC.add_child(Node("q1", 0.7))
	rootC.add_child(Node("q1", 0.9))


	for node in rootC.childs:
		node.add_child(Node("q2", 0.2))
		node.add_child(Node("q2", 0.4))
		node.add_child(Node("q2", 0.72))
		node.add_child(Node("q2", 0.89))


	for q1 in rootC.childs:
		for q2 in q1.childs:
			node.add_child(Node("q3", 0.2))
			node.add_child(Node("q3", 0.4))
			node.add_child(Node("q3", 0.72))
			node.add_child(Node("q3", 0.82))

	for q1 in rootC.childs:
		for q2 in q1.childs:
			for q3 in q2.childs:
				node.add_child(Node("q4", 0.2))
				node.add_child(Node("q4", 0.4))
				node.add_child(Node("q4", 0.72))
				node.add_child(Node("q4", 0.82))

	return {rootA, rootB, rootC}

def decide():
	# keluarga, academis, sendiri, lingkungan = 0
	rootA, rootB, rootC = createTree()
	now = rootA
	while(len(now.childs) > 0 ):
		print (now.name+" ? ")
		for chl in now.childs:
			print(chl.name+" ")
		print("\n")
		now = now.childs[1]
	decideCate()
	conq()

def landing(request):
    html = 'landing.html'
    # decide()
    return render(request, html)

def soal(request):
    html = 'soal.html'
    return render(request, html)

@csrf_exempt
def hasil(request):
    # bikin logic nya disini aja
    html = 'hasil.html'
    return render(request, html)