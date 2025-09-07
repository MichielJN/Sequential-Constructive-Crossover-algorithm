import os
import random

def SCX(parent1, parent2, costMatrix):
    child = []
    currentItem = None
    if len(child) == 0:
        currentItem = parent1[0]
        child.append(currentItem)
        
    while len(child) < len(parent1):

        indexParent1 = parent1.index(currentItem)
        indexParent2 = parent2.index(currentItem)
        indexSuccesor1 = None
        indexSuccesor2 = None
        if indexParent1 == len(parent1) -1:
            indexSuccesor1 = 0
        else:
            indexSuccesor1 = indexParent1 + 1  

        if indexParent2 == len(parent2) -1:
            indexSuccesor2 = 0
        else:
            indexSuccesor2 = indexParent2 + 1          

        items1 = [parent1[indexParent1], parent1[indexSuccesor1]]
        items2 = [parent2[indexParent2], parent2[indexSuccesor2]]
        
        costParent1 = CalculateCost(costMatrix, items1)
        costParent2 = CalculateCost(costMatrix, items2)

        if child.__contains__(parent1[indexSuccesor1]) and child.__contains__(parent2[indexSuccesor2]):
            currentItem = [item for item in parent1 if item not in child][0]
            child.append(currentItem)
        elif child.__contains__(parent1[indexSuccesor1]):
            child.append(items2[1])    
            currentItem = items2[1]
        elif child.__contains__(parent2[indexSuccesor2]):
            child.append(items1[1])
            currentItem = items1[1]
        else:
            if costParent1 <= costParent2:
                child.append(items1[1])
                currentItem = items1[1]
            else:
                child.append(items2[1])    
                currentItem = items2[1]

    return child
        
def GetRandomList(itemSet):
    itemSet = itemSet.copy()
    for i in range(0, len(itemSet) * 100):
        index = random.randint(0, len(itemSet)-1)
        item = itemSet[index]
        itemSet.pop(index)
        index = random.randint(0, len(itemSet)-1)
        itemSet.insert(index, item)
    return itemSet

def CalculateCost(costMatrix, items):
    cost = { (a, b): c for (a, b, c) in costMatrix }
    return cost[(items[0], items[1])]     


itemSet = ["A", "B", "C", "D", "E"]
costMatrix = [
    ('A','B',8), ('A','C',3), ('A','D',6), ('A','E',2),
    ('B','A',8), ('B','C',5), ('B','D',4), ('B','E',7),
    ('C','A',3), ('C','B',5), ('C','D',2), ('C','E',6),
    ('D','A',6), ('D','B',4), ('D','C',2), ('D','E',5),
    ('E','A',2), ('E','B',7), ('E','C',6), ('E','D',5),
]

parent1 = GetRandomList(itemSet)
parent2 = GetRandomList(itemSet)

for i in range (0, 119):
    parent1 = SCX(parent1, parent2, costMatrix)
    parent2 = SCX(parent2, parent1, costMatrix)

print(SCX(parent1, parent2, costMatrix))

     





    
