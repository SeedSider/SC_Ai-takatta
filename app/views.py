from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
from .dataconstructor import *
from django.views.decorators.csrf import csrf_exempt

from collections import defaultdict, Counter
import itertools
import math
import csv
import random

T = bool(True)
F = bool(False)

def landing(request):
    html = 'landing.html'
    # decide()
    return render(request, html)

def game(request):
    html = 'game.html'
    return render(request, html)

def soal(request):
    html = 'soal.html'
    return render(request, html)

@csrf_exempt
def hasil(request):
    # bikin logic nya disini aja
    net = (BayesNet()
    .add('a1',[], 0.1)
    .add('a2',[], 0.1)
    .add('a3',[], 0.1)
    .add('a4',[], 0.1)
    .add('a5',[], 0.1)
    .add('a6',[], 0.1)
    )

    dct = {}
    with open('app/static/data/dataset.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tmp = []
	        # print(row)
            if(row[0][0]=='Q'):
                continue
            for i in range(len(row)):
                if(row[i][0]=='T'):
                    tmp.append(T)
                elif i>5:
                    tmp.append(row[i])
                else:
                    tmp.append(F)
            key = (tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5])
	        # print(key)
            dct[key]= float(tmp[12])
	        # print (dct)

	# print(dct)
    net.add('a7', ['a1','a2','a3','a4','a5','a6'], dct)

	# alarm_net = (BayesNet()
	#     .add('Burglary', [], 0.001)
	#     .add('Earthquake', [], 0.002)
	#     .add('Alarm', ['Burglary', 'Earthquake'], {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001})
	#     .add('JohnCalls', ['Alarm'], {T: 0.90, F: 0.05})
	#     .add('MaryCalls', ['Alarm'], {T: 0.70, F: 0.01}))

    # globalize(alarm_net.lookup) 
	# print(alarm_net.variables)
	# print(P(Burglary))
    
    globalize(net.lookup) 
    print(net.variables)
    print(P(a7, {a1:F, a2:F, a3:T, a4:T,  a5:T, a6:T}))
	# print(a7.cpt)
    bayesNetwork = generateBayesNetwork()
    print(bayesNetwork)
    answer = request.POST
    print(answer)
    html = 'hasil.html'
    return render(request, html)

class BayesNet(object):
    "Bayesian network: a graph of variables connected by parent links."
     
    def __init__(self): 
        self.variables = [] # List of variables, in parent-first topological sort order
        self.lookup = {}    # Mapping of {variable_name: variable} pairs
            
    def add(self, name, parentnames, cpt):
        "Add a new Variable to the BayesNet. Parentnames must have been added previously."
        parents = [self.lookup[name] for name in parentnames]
        var = Variable(name, cpt, parents)
        self.variables.append(var)
        self.lookup[name] = var
        return self
    
class Variable(object):
    "A discrete random variable; conditional on zero or more parent Variables."
    
    def __init__(self, name, cpt, parents=()):
        "A variable has a name, list of parent variables, and a Conditional Probability Table."
        self.__name__ = name
        self.parents  = parents
        self.cpt      = CPTable(cpt, parents)
        self.domain   = set(itertools.chain(*self.cpt.values())) # All the outcomes in the CPT
                
    def __repr__(self): return self.__name__
    
class Factor(dict): "An {outcome: frequency} mapping."

class ProbDist(Factor):
    """A Probability Distribution is an {outcome: probability} mapping. 
    The values are normalized to sum to 1.
    ProbDist(0.75) is an abbreviation for ProbDist({T: 0.75, F: 0.25})."""
    def __init__(self, mapping=(), **kwargs):
        if isinstance(mapping, float):
            mapping = {T: mapping, F: 1 - mapping}
        self.update(mapping, **kwargs)
        normalize(self)
        
class Evidence(dict): 
    "A {variable: value} mapping, describing what we know for sure."
        
class CPTable(dict):
    "A mapping of {row: ProbDist, ...} where each row is a tuple of values of the parent variables."
    
    def __init__(self, mapping, parents=()):
        """Provides two shortcuts for writing a Conditional Probability Table. 
        With no parents, CPTable(dist) means CPTable({(): dist}).
        With one parent, CPTable({val: dist,...}) means CPTable({(val,): dist,...})."""
        if len(parents) == 0 and not (isinstance(mapping, dict) and set(mapping.keys()) == {()}):
            mapping = {(): mapping}
        for (row, dist) in mapping.items():
            if len(parents) == 1 and not isinstance(row, tuple): 
                row = (row,)
            self[row] = ProbDist(dist)

class Bool(int):
    "Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'"
    __str__ = __repr__ = lambda self: 'T' if self else 'F'
def P(var, evidence={}):
    "The probability distribution for P(variable | evidence), when all parent variables are known (in evidence)."
    row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row]

def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist

def sample(probdist):
    "Randomly sample an outcome from a probability distribution."
    r = random.random() # r is a random point in the probability distribution
    c = 0.0             # c is the cumulative probability of outcomes seen so far
    for outcome in probdist:
        c += probdist[outcome]
        if r <= c:
            return outcome
        
def globalize(mapping):
    "Given a {name: value} mapping, export all the names to the `globals()` namespace."
    globals().update(mapping)
