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

response = {}

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
    
    globalize(net.lookup) 

    bayesNetwork = generateBayesNetwork()
    answer = dict(request.POST)
    val1 = getData(answer.__getitem__('1'))
    val2 = getData(answer.__getitem__('2'))
    val3 = getData(answer.__getitem__('3'))
    val4 = getData(answer.__getitem__('4'))
    val5 = getData(answer.__getitem__('5'))
    val6 = getData(answer.__getitem__('6'))

    dataInput = {a1:val1, a2:val2, a3:val3, a4:val4,  a5:val5, a6:val6}
    dataResult = {key: value for key, value in dataInput.items() if value is not None}
    bayesValue = enumeration_ask(a7, dataResult, net)[T] * 100
    print(dataResult)
    print(enumeration_ask(a7, {a1:F, a2:F, a3:F, a4:F, a5:F, a6:F}, net)[T]*100)
    response['test'] = float("{0:.2f}".format(bayesValue))

    html = 'hasil.html'
    return render(request, html, response)



def getData(object):
	if object == ['Iya']:
		return T
	elif object == ['Tidak']:
		return F
	else:
		return

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

def joint_distribution(net):
    "Given a Bayes net, create the joint distribution over all variables."
    return ProbDist({row: prod(P_xi_given_parents(var, row, net)
                               for var in net.variables)
                     for row in all_rows(net)})

def all_rows(net): return itertools.product(*[var.domain for var in net.variables])

def P_xi_given_parents(var, row, net):
    "The probability that var = xi, given the values in this row."
    dist = P(var, Evidence(zip(net.variables, row)))
    xi = row[net.variables.index(var)]
    return dist[xi]

def prod(numbers):
    "The product of numbers: prod([2, 3, 5]) == 30. Analogous to `sum([2, 3, 5]) == 10`."
    result = 1
    for x in numbers:
        result *= x
    return result

def enumeration_ask(X, evidence, net):
    "The probability distribution for query variable X in a belief net, given evidence."
    i    = net.variables.index(X) # The index of the query variable X in the row
    dist = defaultdict(float)     # The resulting probability distribution over X
    for (row, p) in joint_distribution(net).items():
        if matches_evidence(row, evidence, net):
            dist[row[i]] += p
    return ProbDist(dist)

def matches_evidence(row, evidence, net):
    "Does the tuple of values for this row agree with the evidence?"
    return all(evidence[v] == row[net.variables.index(v)]
               for v in evidence)