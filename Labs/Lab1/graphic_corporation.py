# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:09:39 2018

@author: pengshi
"""
from decisiontrees import Node
# Parameters for the decision tree
okay=.92

pos_when_okay=.7
neu_when_okay=.2
neg_when_okay=.1

pos_when_fail=.15
neu_when_fail=.1
neg_when_fail=.75

revenue=1050
baseCost=600
precautionCost=720
rebuildCost=150
reinstallCost=210
testCost=20
failCost=100

def buildTree():
    ''' The function builds the decision tree for the Graphic corporation case, given certain parameters '''
    
    # Calculate the relevant probabilities: pos_okay=P(pos and okay), okay_when_pos=P(okay|pos), posProb=P(pos)
    fail=1-okay
    pos_okay=okay*pos_when_okay
    pos_fail=fail*pos_when_fail
    neu_okay=okay*neu_when_okay
    neu_fail=fail*neu_when_fail
    neg_okay=okay*neg_when_okay
    neg_fail=fail*neg_when_fail

    okay_when_pos=pos_okay/(pos_okay+pos_fail)
    okay_when_neu=neu_okay/(neu_okay+neu_fail)
    okay_when_neg=neg_okay/(neg_okay+neg_fail)
    
    posProb=pos_okay+pos_fail
    neuProb=neu_okay+neu_fail
    negProb=neg_okay+neg_fail
    
    # Build the tree. For outcome nodes, we assign the value, which is the net profit from that outcome. 
    # For decision nodes, we give a list of children (branches from the node corresponding to possible decisions).
    # For event nodes, we give first a list of the children, then a list of the corresponding probabilities.
    pos_fail=Node('fail',value=revenue-baseCost-rebuildCost-reinstallCost-testCost-failCost)
    pos_succeed=Node('succeed',value=revenue-baseCost-testCost)
    pos_rebuild=Node('rebuild',value=revenue-baseCost-rebuildCost-testCost)
    pos_normal=Node('sell',[pos_succeed,pos_fail],[okay_when_pos, 1-okay_when_pos])
    pos_root=Node('Test Pos.',[pos_normal,pos_rebuild])

    neu_fail=Node('fail',value=revenue-baseCost-rebuildCost-reinstallCost-testCost-failCost)
    neu_succeed=Node('succeed',value=revenue-baseCost-testCost)
    neu_rebuild=Node('rebuild',value=revenue-baseCost-rebuildCost-testCost)
    neu_normal=Node('sell',[neu_succeed,neu_fail],[okay_when_neu,1-okay_when_neu])
    neu_root=Node('Test Neu.',[neu_normal,neu_rebuild])

    neg_fail=Node('fail',value=revenue-baseCost-rebuildCost-reinstallCost-testCost-failCost)
    neg_succeed=Node('succeed',value=revenue-baseCost-testCost)
    neg_rebuild=Node('rebuild',value=revenue-baseCost-rebuildCost-testCost)
    neg_normal=Node('sell',[neg_succeed,neg_fail],[okay_when_neg,1-okay_when_neg])
    neg_root=Node('Test Neg.',[neg_normal,neg_rebuild])

    precaution=Node('precaution',value=revenue-precautionCost)
    fail=Node('fail',value=revenue-baseCost-rebuildCost-reinstallCost-failCost)
    succeed=Node('succeed',value=revenue-baseCost)
    normal=Node('normal',[succeed,fail],[okay,1-okay])

    normal_test=Node('normal+test',[pos_root,neu_root,neg_root],[posProb,neuProb,negProb])
    tree=Node('Dana',[precaution,normal,normal_test])
    return tree

tree=buildTree()
graph=tree.graph()
display(graph)
