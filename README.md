👀 Thank you for your time learning about my substance! ~brianh  
👀 👋  this page => code  

---------

Computer science departments should consider assessing students' programming skills each year and having learning modules to address missing skills. I am happy to elaborate on the 5 core modules I am building to address this need.  

One core is data transformation, including indexing, positionality, and read / reporting basics of text and csv data in R and Python. https://en.wikipedia.org/wiki/Data_transformation_(computing)  

--------
Part I of VII, self-paced training modules on Python's classes, conditionals, data objects, functions, iterators, libraries, and transformers.  
👀   7 Pillars of Python  
👀 👋 7 Pillars of R (expected 12.31.22)  

7 Pillars focuses on Python because can cast unfamiliar data objects to Python built-ins (dictionary, list, etc).
Students quickly GET this.

Page 1 of zion code book associated with it.

-----------
![7_pillars](https://user-images.githubusercontent.com/59778456/200092472-1e7b6db7-0e17-4caa-bc10-90751f194708.JPG)

def binary_search():  
    """ #ID.1 = binary.search.algorithm  
    Created on Thu Jan 26 20:06:50 2023  
    @author: 17574, b.hogan@snhu.edu  
    """  

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


--------------
**Portfolio**  
• coach_tutor_volunteer_____https://github.com/bbe2/portfolio/tree/coach_tutor_volunteer  
• code training an samples_https://github.com/bbe2/portfolio/tree/code  
• Google Prof. ML Cert_____https://github.com/bbe2/portfolio/tree/google_Prof_ML_eng_cert  
• master of science port____https://github.com/bbe2/portfolio/tree/master_portfolio  
• multimedia_styleguide___https://github.com/bbe2/portfolio/tree/multimedia_styleguide  
• re-engineering____________https://github.com/bbe2/portfolio/tree/reengineering  
• reference_recommend____https://github.com/bbe2/portfolio/tree/reference_recommend  
• research_experience______https://github.com/bbe2/portfolio/tree/research_experience  
• scientific_editing__________https://github.com/bbe2/portfolio/tree/scientific_edit  
• teaching___________________https://github.com/bbe2/portfolio/tree/teaching  
• technical writing__________https://github.com/bbe2/portfolio/tree/tech_write  
• tech curriculum + Grow w Google__https://github.com/bbe2/portfolio/tree/tech_curriculum_an_GwG  
• >_7.Pillars.of.Python______https://github.com/bbe2/portfolio/tree/%3E_7_Pillars_of_Python  
