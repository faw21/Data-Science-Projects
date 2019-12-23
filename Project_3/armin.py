# CS 1656 Assignment #3
# Fangzheng Wu
# Nov 18 2019
# Prof. Alexandros Labrinidis

# Usage: python3 armin.py input_file_name output_file_name min_support_prcentage min_confindence

import itertools
import csv
import sys


def tupleToString(tup):
    string = ''
    for element in tup:
        string = string+str(element)+','
    string = string[:-1]
    return string

#Assign arguments
inFileName = sys.argv[1]
outFileName = sys.argv[2]
min_support_percentage = float(sys.argv[3])
min_confidence = float(sys.argv[4])

#Create a list to store all transactions
transactions = []
with open(inFileName,'r') as inFile:
    reader = csv.reader(inFile)
    for item in reader:
        item.pop(0)
        transactions.append(item)
transactions.sort()

#Create a set to store all items in transaction
#Use set since it does not allow duplicate
items = set()
for transaction in transactions:
    for item in transaction:
        items.add(item)

#Then convert the set to list and sort it 
items = list(items)
items.sort()


#get every possible combination(item set) of items
#e.g.: permutation[0]: ['A', 'B', 'C', 'D', 'E', 'F']
#permutation[1]: [('A','B'),('A','C'),('A','D')....]
#permutation[2]: [('A','B','C'),('A','B','D')....]
permutation = []
for x in range(1,len(items)+1):
    permutation.append(list(itertools.combinations(items, x)))\


#create list of Cadidate Frequent Item & Verified Frequent Item
CFI = [items,]
VFI = []

#Verify itemsets with only one item
newDictionary = {}
for item in CFI[0]:
    count = 0
    for transaction in transactions:
        if item in transaction: #if the item is in one transaction, increment the count
            count = count+1

    #after iterating through the transactions, if the sup(item) is greater than/equal to
    #min_support_percentage, add this item as a tuple to the dictionary (item tuple is the key, sup(item) is the value)
    support_percentage = count/len(transactions)
    if support_percentage>=min_support_percentage :
        newDictionary[(item,)] = support_percentage

#append the dictionary in the VFI list
VFI.append(newDictionary)

#Verify itemsets with n items (1 < n <= number of items)
for i in range(1,len(items)):
    newDictionary = {}
    newList = []
    for itemset in permutation[i]: #permutation[i] contains all possible itemsets with i+1 items
        proceed = True

        #given itemset with i+1 items,
        #generate all possible sub-itemsets with i items
        for sub_itemset in list(itertools.combinations(itemset, i)):
        
            #if all sub-itemset is in the VFI list, then add the itemset to CFI
            if sub_itemset not in VFI[i-1]:
                proceed = False
                break
        if proceed:
            newList.append(itemset)
    CFI.append(newList)
    

    #CFI[i] contains all candidate itemsets with i+1 items
    for itemset in CFI[i]:
        min_ssup = 1
        count = 0
        
        for transaction in transactions:
            proceed = True

            #if all items in one itemset are included in one transaction, count++
            for item in itemset:
                if item not in transaction:
                    proceed = False
                    break
            if proceed == True:
                count = count+1

        #calculate supp()        
        support_percentage = count/len(transactions)
        if support_percentage>=min_support_percentage :
            newDictionary[itemset] = support_percentage
    
    #finish adding itemsets to VFI       
    VFI.append(newDictionary)

#Create a list to store all association rule combination
association_rule = []


for i in range(1, len(items)):
    #VFI[i] is a dictionary contains all verified frequent itemsets with i+1 items
    #VFI[i].keys() returns all keys (all tuples of itemsets)
    itemsets = VFI[i].keys()
    for itemset in itemsets:
        #given itemset, generate all possible sub_itemsets (with any length)
        sub_itemsets = []
        for j in range(1,i+1):
            sub_itemsets = sub_itemsets + list(itertools.combinations(itemset, j))
        
        
        #select every sub_itemset as left sub_itemset in the association rule
        for sub_itemset_left in sub_itemsets:
            
            #then get the right sub_itemset in the association rule 
            #by doing sub_item_right = itemset - sub_itemset_left
            sub_itemset_right = ()
            for item in itemset:
                if item not in sub_itemset_left:
                    sub_itemset_right = sub_itemset_right + (item,)

                    
            #sup1 is the support number of sub_itemset_left
            sup1 = 0
            for transaction in transactions:
                proceed = True
                for item in sub_itemset_left:
                    if item not in transaction:
                        proceed = False
                        break
                if proceed == True:
                    sup1 = sup1+1
            
            #sup2 is the support number of (sub_left and sub_right)      
            sup2 = 0
            for transaction in transactions:
                proceed = True
                for item in itemset:
                    if item not in transaction:
                        proceed = False
                        break
                if proceed == True:
                    sup2 = sup2+1
            
            
            #compute confidence
                
                #if confidence is greater than/equal to min_confindence, 
                #add support_percentage of itemset, confidence of itemset, sub_left, sub_right
                #to the list of association rule
            confidence = sup2/sup1
            if confidence >= min_confidence:
                association_rule.append((VFI[i][itemset], confidence, sub_itemset_left, sub_itemset_right))


#write to the output file
with open(outFileName,'w') as outFile:
    writer = csv.writer(outFile)
    for item in VFI:
        if len(item)>0:
            for row in item:
                outFile.write('S,%.4f,%s%s' %(item[row], tupleToString(row), '\n'))
    for item in association_rule:
        outFile.write('R,%.4f,%.4f,%s,\'=>\',%s%s'%(item[0],item[1],tupleToString(item[2]),tupleToString(item[3]),'\n'))