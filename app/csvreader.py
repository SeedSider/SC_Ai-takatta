import csv
from .node import Node
from enum import Enum

data = []

class Option(Enum):
    stress = 0
    opt1 = 1
    opt2 = 2
    opt3 = 3
    opt4 = 4
    opt5 = 5
    opt6 = 6

def readCSV():
    node_dict = {}
    node_list = []
    with open('/data/dataset.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            node_dict[(row[0], row[1], row[2], row[3], row[4], row[5])] = row[12]
    node = Node('stress', '1 2 3 4 5 6', node_dict)
    node_list.append(node)
    bayesNet = BayesianNetwork(node_list)
    return bayesNet