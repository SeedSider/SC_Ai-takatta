import csv
from .node import Node
from .bayesian import BayesianNetwork
import os
from django.conf import settings

def generateBayesNetwork():
    rootDatasetDir = settings.BASE_DIR + '/static/data/dataset-all-factors.csv'
    leafDatasetDir = settings.BASE_DIR + '/app/static/data/dataset-stress-given-all-factors.csv'    
    rootNodesList = rootNodes(rootDatasetDir)
    leafNodesList = leafNodes(leafDatasetDir)
    allNodes = rootNodesList + leafNodesList
    bayesNet = BayesianNetwork(allNodes)
    return bayesNet

def rootNodes(file):
    node_list = []
    node_dict = {}        
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in readCSV:
            if (i != 0):
                node_dict[True] =  float(row[1])
                node_dict[False] = float(row[2])
                node = Node(row[0], '', node_dict)
                node_list.append(node)
            i += 1
    return node_list

def leafNodes(file):
    node_list = []
    node_dict = {}    
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in readCSV:
            if (i != 0):
                node_dict[(row[0] == "TRUE", row[1] == "TRUE", row[2] == "TRUE", row[3] == "TRUE", row[4] == "TRUE", row[5] == "TRUE")] = float(row[12])
            i += 1
    node = Node('Stress', 'Q1 Q2 Q3 Q4 Q5 Q6', node_dict)
    node_list.append(node)
    return node_list