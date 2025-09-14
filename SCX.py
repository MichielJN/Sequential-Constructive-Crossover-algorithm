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
            itemToUse = Fallback(parent1, parent2, child, indexSuccesor1, indexSuccesor2, costMatrix)
            child.append(itemToUse)
            currentItem = itemToUse
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

def Fallback(parent1, parent2, child, indexSuccesor1, indexSuccesor2, costMatrix):
    unusedItems = [item for item in parent1 if item not in child]
    if len(unusedItems) == 1:
        return unusedItems[0]
    itemToUse = None
    if len(child) == len(parent1)-1:
        for item in unusedItems:
            itemRow = [child[len(child)-1], item, child[0]]
            points = CalculateCost(costMatrix, [itemRow[0], itemRow[1]]) + CalculateCost(costMatrix, [itemRow[1], itemRow[2]])
            if itemToUse == None:
                itemToUse = [item, points]
            elif points < itemToUse[1]:
                itemToUse = [item, points]
    else:
        for item in unusedItems:
            points = CalculateCost(costMatrix, [child[len(child)-1], item])
            if itemToUse == None:
                itemToUse = [item, points]
            elif points < itemToUse[1]:
                itemToUse = [item, points]
    return itemToUse[0]
        
def CalculateCost(costMatrix, items):
    cost = { (a, b): c for (a, b, c) in costMatrix }
    return cost[(items[0], items[1])]     

def CalculateRouteCost(child, costMatrix):
    cost = 0
    costPairs = []
    for i in range(0, len(child)):
        if i == len(child) - 1:
            costPairs.append([child[i], child[0]])
        else:    
            costPairs.append([child[i], child[i+1]])
    for i in costPairs:
        cost += CalculateCost(costMatrix, i)
    return cost

def SortListOnLowestCost(parents, costMatrix):
    selectedParents = []
    for i in range(0, len(parents)):
        item = parents.pop()
        item = list(item)
        selectedParents.append([item, CalculateRouteCost(item, costMatrix)])
    selectedParents.sort(key=lambda x : x[1])
    selectedParents = [i[0] for i in selectedParents]    
    return selectedParents

def GeneticAlgorithm(itemSet, costMatrix, startingPopulation, populationDivider):
    parents = set()
    bestParent = None
    while len(parents) < startingPopulation  +1 / populationDivider:
        random.shuffle(itemSet)
        parents.add(tuple(itemSet))

    selectedParents = SortListOnLowestCost(parents, costMatrix)    

    selectedParents = selectedParents[:int(len(selectedParents)/ 2)]
    children = []
    while len(selectedParents) > 1:
        for i in range(0, len(selectedParents), 2):
            if len(selectedParents) % 2 == 1 and i == len(selectedParents)-1 :
                children.append(SCX(selectedParents[i], selectedParents[0], costMatrix))
                children.append(SCX(selectedParents[0], selectedParents[i], costMatrix))
            else:
                children.append(SCX(selectedParents[i], selectedParents[i+1], costMatrix))
                children.append(SCX(selectedParents[i+1], selectedParents[i], costMatrix))  

        bestParent = selectedParents[0]
        selectedParents = SortListOnLowestCost(children, costMatrix)[:int(len(selectedParents)/ populationDivider)]
        children.clear()
    if len(selectedParents) == 0:
        return bestParent
    else:
        return selectedParents[0]

# itemSet = ["A", "B", "C", "D", "E"]
# costMatrix = [
#      ('A','B',8), ('A','C',3), ('A','D',6), ('A','E',2),
#      ('B','A',8), ('B','C',5), ('B','D',4), ('B','E',7),
#      ('C','A',3), ('C','B',5), ('C','D',2), ('C','E',6),
#      ('D','A',6), ('D','B',4), ('D','C',2), ('D','E',5),
#      ('E','A',2), ('E','B',7), ('E','C',6), ('E','D',5),
# ]
itemSet = ['A','B','C','D','E','F','G','H','I','J',
           'K','L','M','N','O','P','Q','R','S','T']

costMatrix = [
    ('A','B',12), ('A','C',5), ('A','D',17), ('A','E',8), ('A','F',19), ('A','G',14), ('A','H',9), ('A','I',4), ('A','J',11),
    ('A','K',16), ('A','L',7), ('A','M',13), ('A','N',10), ('A','O',18), ('A','P',6), ('A','Q',15), ('A','R',20), ('A','S',3), ('A','T',9),

    ('B','A',12), ('B','C',9), ('B','D',3), ('B','E',14), ('B','F',7), ('B','G',16), ('B','H',12), ('B','I',18), ('B','J',6),
    ('B','K',11), ('B','L',13), ('B','M',5), ('B','N',15), ('B','O',19), ('B','P',4), ('B','Q',17), ('B','R',8), ('B','S',20), ('B','T',10),

    ('C','A',5), ('C','B',9), ('C','D',12), ('C','E',6), ('C','F',18), ('C','G',7), ('C','H',15), ('C','I',10), ('C','J',14),
    ('C','K',8), ('C','L',19), ('C','M',11), ('C','N',13), ('C','O',16), ('C','P',20), ('C','Q',4), ('C','R',17), ('C','S',9), ('C','T',5),

    ('D','A',17), ('D','B',3), ('D','C',12), ('D','E',11), ('D','F',8), ('D','G',6), ('D','H',19), ('D','I',13), ('D','J',7),
    ('D','K',10), ('D','L',15), ('D','M',9), ('D','N',4), ('D','O',14), ('D','P',18), ('D','Q',5), ('D','R',20), ('D','S',16), ('D','T',12),

    ('E','A',8), ('E','B',14), ('E','C',6), ('E','D',11), ('E','F',10), ('E','G',4), ('E','H',13), ('E','I',7), ('E','J',16),
    ('E','K',18), ('E','L',5), ('E','M',20), ('E','N',15), ('E','O',9), ('E','P',17), ('E','Q',19), ('E','R',12), ('E','S',3), ('E','T',14),

    ('F','A',19), ('F','B',7), ('F','C',18), ('F','D',8), ('F','E',10), ('F','G',15), ('F','H',4), ('F','I',20), ('F','J',12),
    ('F','K',6), ('F','L',9), ('F','M',14), ('F','N',13), ('F','O',11), ('F','P',16), ('F','Q',5), ('F','R',17), ('F','S',19), ('F','T',7),

    ('G','A',14), ('G','B',16), ('G','C',7), ('G','D',6), ('G','E',4), ('G','F',15), ('G','H',8), ('G','I',18), ('G','J',20),
    ('G','K',5), ('G','L',11), ('G','M',13), ('G','N',9), ('G','O',17), ('G','P',10), ('G','Q',12), ('G','R',19), ('G','S',3), ('G','T',16),

    ('H','A',9), ('H','B',12), ('H','C',15), ('H','D',19), ('H','E',13), ('H','F',4), ('H','G',8), ('H','I',7), ('H','J',11),
    ('H','K',20), ('H','L',16), ('H','M',18), ('H','N',14), ('H','O',6), ('H','P',12), ('H','Q',9), ('H','R',5), ('H','S',17), ('H','T',10),

    ('I','A',4), ('I','B',18), ('I','C',10), ('I','D',13), ('I','E',7), ('I','F',20), ('I','G',18), ('I','H',7), ('I','J',9),
    ('I','K',14), ('I','L',6), ('I','M',12), ('I','N',19), ('I','O',8), ('I','P',15), ('I','Q',5), ('I','R',11), ('I','S',16), ('I','T',13),

    ('J','A',11), ('J','B',6), ('J','C',14), ('J','D',7), ('J','E',16), ('J','F',12), ('J','G',20), ('J','H',11), ('J','I',9),
    ('J','K',13), ('J','L',19), ('J','M',4), ('J','N',17), ('J','O',5), ('J','P',15), ('J','Q',8), ('J','R',10), ('J','S',18), ('J','T',6),

    ('K','A',16), ('K','B',11), ('K','C',8), ('K','D',10), ('K','E',18), ('K','F',6), ('K','G',5), ('K','H',20), ('K','I',14),
    ('K','J',13), ('K','L',7), ('K','M',15), ('K','N',12), ('K','O',9), ('K','P',17), ('K','Q',16), ('K','R',19), ('K','S',4), ('K','T',20),

    ('L','A',7), ('L','B',13), ('L','C',19), ('L','D',15), ('L','E',5), ('L','F',9), ('L','G',11), ('L','H',16), ('L','I',6),
    ('L','J',19), ('L','K',7), ('L','M',14), ('L','N',10), ('L','O',12), ('L','P',20), ('L','Q',8), ('L','R',17), ('L','S',18), ('L','T',3),

    ('M','A',13), ('M','B',5), ('M','C',11), ('M','D',9), ('M','E',20), ('M','F',14), ('M','G',13), ('M','H',18), ('M','I',12),
    ('M','J',4), ('M','K',15), ('M','L',14), ('M','N',19), ('M','O',6), ('M','P',11), ('M','Q',7), ('M','R',10), ('M','S',8), ('M','T',16),

    ('N','A',10), ('N','B',15), ('N','C',13), ('N','D',4), ('N','E',15), ('N','F',13), ('N','G',9), ('N','H',14), ('N','I',19),
    ('N','J',17), ('N','K',12), ('N','L',10), ('N','M',19), ('N','O',7), ('N','P',16), ('N','Q',18), ('N','R',5), ('N','S',20), ('N','T',11),

    ('O','A',18), ('O','B',19), ('O','C',16), ('O','D',14), ('O','E',9), ('O','F',11), ('O','G',17), ('O','H',6), ('O','I',8),
    ('O','J',5), ('O','K',9), ('O','L',12), ('O','M',6), ('O','N',7), ('O','P',10), ('O','Q',15), ('O','R',20), ('O','S',13), ('O','T',19),

    ('P','A',6), ('P','B',4), ('P','C',20), ('P','D',18), ('P','E',17), ('P','F',16), ('P','G',10), ('P','H',12), ('P','I',15),
    ('P','J',15), ('P','K',17), ('P','L',20), ('P','M',11), ('P','N',16), ('P','O',10), ('P','Q',14), ('P','R',8), ('P','S',9), ('P','T',5),

    ('Q','A',15), ('Q','B',17), ('Q','C',4), ('Q','D',5), ('Q','E',19), ('Q','F',5), ('Q','G',12), ('Q','H',9), ('Q','I',5),
    ('Q','J',8), ('Q','K',16), ('Q','L',8), ('Q','M',7), ('Q','N',18), ('Q','O',15), ('Q','P',14), ('Q','R',20), ('Q','S',6), ('Q','T',11),

    ('R','A',20), ('R','B',8), ('R','C',17), ('R','D',20), ('R','E',12), ('R','F',17), ('R','G',19), ('R','H',5), ('R','I',11),
    ('R','J',10), ('R','K',19), ('R','L',17), ('R','M',10), ('R','N',5), ('R','O',20), ('R','P',8), ('R','Q',20), ('R','S',7), ('R','T',16),

    ('S','A',3), ('S','B',20), ('S','C',9), ('S','D',16), ('S','E',3), ('S','F',19), ('S','G',3), ('S','H',17), ('S','I',16),
    ('S','J',18), ('S','K',4), ('S','L',18), ('S','M',8), ('S','N',20), ('S','O',13), ('S','P',9), ('S','Q',6), ('S','R',7), ('S','T',14),

    ('T','A',9), ('T','B',10), ('T','C',5), ('T','D',12), ('T','E',14), ('T','F',7), ('T','G',16), ('T','H',10), ('T','I',13),
    ('T','J',6), ('T','K',20), ('T','L',3), ('T','M',16), ('T','N',11), ('T','O',19), ('T','P',5), ('T','Q',11), ('T','R',16), ('T','S',14),
]
child = GeneticAlgorithm(itemSet, costMatrix, 1000, 8)
costChild = CalculateRouteCost(child, costMatrix)
print(child)
print(costChild)