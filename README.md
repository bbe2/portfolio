👀 Thank you for your time learning about my substance! ~brianh  
👀 👋  this page => code  

---------

Computer science departments should consider assessing students' programming skills each year and having learning modules to address missing skills. I am happy to elaborate on the 5 core modules I'm designing to address this essential need before ChatGPT solves it all! :)  

One core is data transformation, including indexing, positionality, and read / reporting basics of text and csv data in R and Python. https://en.wikipedia.org/wiki/Data_transformation_(computing)  

--------
Part I of VII, self-paced training modules on Python's classes, conditionals, data objects, functions, iterators, libraries, and transformers.  
👀   7 Pillars of Python  
👀 👋 7 Pillars of R (expected 3Q23)  

7 Pillars focuses on Python because can cast unfamiliar data objects to Python built-ins (dictionary, list, etc).
Students quickly GET this.

zipper (python): [zipper.pdf](https://github.com/bbe2/portfolio/files/10711992/zipper.pdf)


-----------
![7_pillars](https://user-images.githubusercontent.com/59778456/200092472-1e7b6db7-0e17-4caa-bc10-90751f194708.JPG)


### some computer science departments want to see writing of core scripts even if available in common libraries  
i don't disagree, but feel it should be part of a cheatsheet with purpose, variations, how to know if working right, and what current libraries perform it well. In the last month alone (from 02.04.23) I've experience 8 students discussing how they use ChatGPT to survive coding classes but do so with a low retention rate. There needs to be a balance towards solving the problem and getting assistance as needed until more advanced  

**def binary_search():**  
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

![classification](https://user-images.githubusercontent.com/59778456/226056510-b2d13981-614f-4b64-9d6e-85b8d2ed115d.png)

![weird](https://user-images.githubusercontent.com/59778456/226056427-3abf90f0-5080-4f42-92e3-196b2a6b2944.JPG)

--------------
**Portfolio**  https://github.com/bbe2/portfolio  
• tutor.an.volunteer_________https://github.com/bbe2/portfolio/tree/coach_tutor_volunteer  
• code_______________________https://github.com/bbe2/portfolio/tree/code  
• google.content.writer_____https://github.com/bbe2/portfolio/tree/tech_curriculum_an_GwG  
• google.ML.certification___https://github.com/bbe2/portfolio/tree/google_Prof_ML_eng_cert  
• master.of.science.port_____https://github.com/bbe2/portfolio/tree/master_portfolio  
• multimedia.styleguide_____https://github.com/bbe2/portfolio/tree/multimedia_styleguide  
• reengineering______________https://github.com/bbe2/portfolio/tree/reengineering  
• recommendations_________https://github.com/bbe2/portfolio/tree/reference_recommend  
• research.experience_______https://github.com/bbe2/portfolio/tree/research_experience  
• scientific.editing___________https://github.com/bbe2/portfolio/tree/scientific_edit  
• teaching___________________https://github.com/bbe2/portfolio/tree/teaching  
• technical.writing___________https://github.com/bbe2/portfolio/tree/tech_write  
• >_7.py.pillars_______________https://github.com/bbe2/portfolio/tree/%3E_7_Pillars_of_Python  
