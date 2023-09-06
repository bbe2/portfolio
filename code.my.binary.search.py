# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 20:06:50 2023
@author: 17574
"""
#b.hogan@snhu.edu

#ID.1 = binary.search.algorithm

def binary_search():
    myMax = int(input("enter max vector length to search: "))
    target = int(input("what value find between 0->max?: "))
    mylist=[]
    i=0
    while i <=(myMax-1):        #0 = position 1
        mylist.append(i); i +=1
    print(len(mylist))
    myreps =[]
    reps = 0
    top,middle,bottom = 0,0,0
    int(top); int(middle); int(bottom)

    top = len(mylist)-1
    
    while top >= bottom:
        middle = round((top + bottom)/2)
        print("middle is: ",middle)
        if mylist[middle] == target:
            reps = reps + 1 
            myreps.append(middle)
            print("target.was: & tot.reps.were:",middle,reps)
            print(myreps)
            return middle
        elif mylist[middle] < target:
            bottom = middle + 1 #reduce to top half of list
            reps = reps + 1 
            myreps.append(bottom)
        else:
            top = middle -1
            reps = reps + 1 
            myreps.append(top)  #reduce to bottom half of list
    return -1
binary_search()


#del mylist
#del myMax


