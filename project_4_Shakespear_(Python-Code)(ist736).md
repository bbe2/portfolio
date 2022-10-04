"""
Created on Fri Sep  6 16:48:34 2019
@author: BBE | Brian Hogan - (final notes 9/10/19_)
Purpose: ist736 Final Project code for Dr. Gates
Sections & Notes: --this file does not run top to bottom but in stages|sorry!
a) html parser both for individual play and building a DTM
b) k-means
c) createing a DTM by 80/20 splitting 37 shakespears plays
    labels were manual as built in panda not index and couldnt figure sorting
d) stopwords worked well - could have expanded counts to whole corpus
    but continually challenged with time as no one on team had an SVM
    working so concentrated getting a corpus built and right datacube
    for machine learning algorithms; some hand jamming to make happen
e) got all dr. gates code running for ward cosine - very fun
f) was not able to build hyperplanes - was VERY frustrating
g) stemming was promising but was behaving funny so scraped all of it
h) didn't both with wordsclouds as done by other team members
i) got ward distance and linkage matrix from dr gates code up and running
j) (LINE 1396) Arthur wanted to make comparison grid-sent him working code
k) decision tree - got ploypot working - was a difficult install
    afraid to even reboot machine until entire project submitted
"""
#!/Users/a212718477/anaconda3/bin/python
# parsecharfile: parse the HTML code of the Shakespeare scripts generated 
# by MIT at http://shakespeare.mit.edu/
# The output is multiple CSV files, one file per character (role). All of that 
# character's words are stored in that file. 
# All uppercase is converted to lowercase, and all punctuation has been removed.
os.getcwd()
os.chdir('c:\\Users\\BBE\\Desktop\\IST736+TextMining\\abc')
from html.parser import HTMLParser
import re

script={} # This is a dictionary of characters and their lines. All of a character's lines are appended together into one string.
speeches=0
class MyHTMLParser(HTMLParser):  # This class parses the HTML script input.
    readyForName=0
    readyForSpeech=0
    stageDirection=0
    charName=''
    speech=''

    def handle_starttag(self, tag, attrs):

        if (tag=='a' and len(attrs)>0 and 'speech' in attrs[0][1]):     # <A NAME=speech1>
            self.readyForName=1
            return (0)
        elif (tag=='a' and len(attrs)>0 and 'speech' not in attrs[0][1]):  # <A NAME=1.1.1>
            return (0)
        elif (tag=='blockquote'):
            self.readyForSpeech=1
            return (0)
        elif (tag=='i'): 
            self.stageDirection=1   
            return(0)
        # The rest of this method handles things we want to ignore...
        if (tag=='html' or tag=='head' or tag=='title' or tag=='meta' or tag=='body'):    return(0)
        if (tag=='h3' or tag=='table'):           return (0)
        if (tag=='p' or tag=='b' or tag=='link'): return(0)
        if (tag=='br' or tag=='tr' or tag=='td'): return(0)
        # ...but this catches things we might want to process, so report them.
        else:
            print("Encountered a start tag:", tag)
            if (len(attrs)>0): print (attrs[0][0], attrs[0][1])

    def handle_endtag(self, tag):
        global speeches

        if (tag=='html' or tag=='head' or tag=='title' or tag=='body'):    return(0)
        if (tag=='h3' or tag=='table'): return (0)
        if (tag=='p' or tag=='b'):    return(0)
        if (tag=='i'):  
            self.stageDirection=0
            return(0)
        elif (tag=='a' and self.readyForName==1): 
            self.readyForName=0
            return(0)
        elif ((tag=='blockquote' and self.readyForSpeech==1) or (tag=='body' and self.readyForSpeech==1)):
            # We have read in one speech by one character. 
            # If the character is new, add append that name to the script dictionary.
            # Then append this speech to the end of that character's speeches, creating one very long speech.
            if (len(self.charName)>0):  # This avoids ending a speech due to a non-terminal <a>
                speeches += 1
                if self.charName not in script:
                    script[self.charName]=self.speech.lstrip().rstrip()
                else:
                    script[self.charName] = ' '.join((script[self.charName], self.speech.lstrip().rstrip()))
#               print ('{0}, {1}'.format(self.charName, self.speech.lstrip().rstrip()))

            # Prepare for the next speech.
            self.readyForSpeech=0
            self.speech=''
            self.charName=''
            return (0)
        elif (tag=='a'): return (0)
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if (self.readyForName==1):  # We're ready for a character's name. Collect it.
            self.charName=re.sub("[^a-zA-Z]+", "", data) # Remove spaces.
            return(0)
        elif (self.stageDirection==1):  # Ignore stage directions.
            return (0)
        elif (self.readyForSpeech==1):  # We're ready for a speech. Collect it, replace hypenated words with???
            self.speech = ' '.join((self.speech, re.sub("[^a-zA-Z ]+", "", data.lstrip().rstrip().lower())))
            return (0)
        elif (data==' ' or data.lstrip().rstrip()=='\n'): return (0)
        # Drop other stuff.
#       print("Encountered some data :{0}:".format(data)) # For diagnostics.
parser = MyHTMLParser()
# Hold both input and output files open while we read and process the input.
# open('hamlet.csv', 'w', newline='') as csvfile:
####with open('hamlet.html', 'r') as htmlfile:
#with open(
#----------------------------------------------------------------------
with open('Much Ado About Nothing Entire Play.htm', 'r') as htmlfile:
    for aline in htmlfile:
        parser.feed(aline)
        # This does all of the work, using methods above.
    # Write each character's words into a file.
    for character in script.keys():    # All of the roles/characters in the play.
        with open('/'.join(('Corpus', character)), 'w') as outf:
            outf.write(script[character])
#print ("The script had {0} characters and {1} speeches.".format(len(script.keys()), speeches))
#-----------------------------------------------------------------
script
#----------------------------------------------------------
all_words=[]
for key in script:
    all_words.append(script[key])  #thi sis how to get the text
filename = "37.txt"  #have to change by hand at the moment
outf = open(filename,'w')
for line in all_words:
    outf.write(line)
outf.close()

            #all_words=[]
            #for line in script:
            #    all_words.append(line)  #this is how to get the chracters & LABLE3S
##################################
            #################################
            ####################################################
os.getcwd()
script

all_words=[]
for key in script:
    all_words.append(script[key])  #thi sis how to get the text
filename = "1.txt"  #have to change by hand at the moment
outf = open(filename,'w')
for line in all_words:
    outf.write(line)
outf.close()

#== comedy
#All's Well That Ends Well Entire Play.htm; As You Like It Entire Play.htm
#Comedy of Errors Entire Play.htm; Cymbeline Entire Play.htm; 
#Love's Labour's Lost Entire Play.htm; Measure for Measure Entire Play.htm
#Merry Wives of Windsor Entire Play.htm; Merchant of Venice Entire Play.htm
#Midsummer Night's Dream Entire Play.htm; Much Ado About Nothing Entire Play.htm
#Pericles Entire Play.htm; Taming of the Shrew Entire Play.htm
#The Tempest Entire Play.htm; Troiles and Cressida Entire Play.htm
#Twelfth Night Entire Play.htm; Two Gentlemen of Verona Entire Play.htm
#Winter's Tale Entire Play.htm
#
##History
#Henry IV, part 1 Entire Play.htm; Henry IV, part 2 Entire Play.htm
#Henry V Entire Play.htm; Henry VI, part 1 Entire Play.htm
#Henry VI, part 2 Entire Play.htm; Henry VI, part 3 Entire Play.htm
#Henry VIII Entire Play.htm; King John Entire Play.htm
#Richard II Entire Play.htm; Richard III Entire Play.htm
##Tragedy
#Antony and Cleopatra Entire Play.htm        ; Coriolanus Entire Play.htm
#Hamlet Entire Play.htm; Julius Caesar Entire Play.htm
#King Lear Entire Play.htm; Macbeth Entire Play.htm
#Othello Entire Play.htm;  Romeo and Juliet Entire Play.htm
#Timon of Athens Entire Play.htm; Titus Andronicus Entire Play.htm
##== comedy
#Comedy of Errors Entire Play.htm; Cymbeline Entire Play.htm; 
#Love's Labour's Lost Entire Play.htm; Measure for Measure Entire Play.htm
#Merry Wives of Windsor Entire Play.htm; Merchant of Venice Entire Play.htm
#Midsummer Night's Dream Entire Play.htm; Much Ado About Nothing Entire Play.htm
#Pericles Entire Play.htm; Taming of the Shrew Entire Play.htm
#The Tempest Entire Play.htm; Troiles and Cressida Entire Play.htm
#Twelfth Night Entire Play.htm; Two Gentlemen of Verona Entire Play.htm
#Winter's Tale Entire Play.htm

##########################################################
######################################
##################
########
###############################################################
# this code eample of tokenization, vectorization, cropus
# k-means, CSV lableing
# distance measures, frequency, normalization, formats
#############################################################################
import nltk
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
os.getcwd()

os.chdir('c:\\Users\BBE\BBE\DATA\Corpus')   #'c:\\Users\BBE\BBE\DATA\Federalist_Papers') 
# this method uses reading by a path
path = "C:\\Users\\BBE\\BBE\\DATA\\Federalist_Papers"  #wow need 2 slashs
path = "C:\\Users\\BBE\\BBE\\DATA\\Corpus" 

#-------------------------------YO A LOT OF WORK FOR THIS ONE
path = "C:\\Users\\BBE\\BBE\\DATA\\aData_Project_Final"

k-means.......................................
os.chdir('c:\\Users\BBE\BBE\DATA\myCorpus')
path = "C:\\Users\\BBE\\BBE\\DATA\\myCorpus" 

#print(os.listdir(path))
# save the lsit
filenamelist = os.listdir(path)
print(type(filenamelist))  #save as a list  #check the type
filenamelist
#need complete paths to work with CountVectorizer...CONSTRAINT OF METHOD
listofcompletefilepaths =[]  #need an empty list
listofjustfilenames = []
for name in os.listdir(path):
    #print(path+ "\\" + name)
    next = path+ "\\" + name
    nextnameL = name.split(".")
    nextname = nextnameL[0]  #this is pretty interesting...
    listofcompletefilepaths.append(next)
    listofjustfilenames.append(nextname)
#print(listofcompletefilepaths)
print(listofjustfilenames)
len(listofjustfilenames)

listofcompletefilepaths

################################ K MEANS
###################################################KMEANS
#####################################-----k means###########################
bbevect3 = CountVectorizer(input='filename')
bbex_dh = bbevect3.fit_transform(listofcompletefilepaths)
bbex_dh.shape
bbecolnames_original = bbevect3.get_feature_names()
bbecorpusDF0 = pd.DataFrame(bbex_dh.toarray(), columns=bbecolnames_original) #ORIGINAL!!!!!!!!!!!!!!!!!!!!!!!!
bbecorpusDF0.shape
len(bbecolnames_original)
bbecleanDF=bbecorpusDF0

bbecleanDF.shape
nostops = []
bbecolnames_new = []   #build a new colmns list
from nltk.tokenize import word_tokenize
stop_words=set(stopwords.words("english"))
stops = []
for name in bbecolnames_original:
    #print("FFFF",name)
    if((name in nostops) or (len(name)<=3)):
        #print("word dropping: ",name)
        bbecleanDF = bbecleanDF.drop([name],axis=1) #cool drop stopword column
        stops.append(name)
                #print(cleanDF)
    else:
        bbecolnames_new.append(name)
print(stops)
len(bbecolnames_new)
bbecolnames_new
##############################################
#########  STEMMING
#########           ############################################
#from nltk.stem.wordnet import WordNetLemmatizer    
#lem = WordNetLemmatizer() #method we are using
#word = "flying"
#print("Lemmatized Word:",lem.lemmatize(word,"v"))  #v is for verb 
from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()        #print("Stemmed Word:",stem.stem(word))
change_tracker=[]

bbecolnames_new[0:50] #list of words to debug this stemming...
len(bbecolnames_new)
bbecleanDF

word_family = []
skip_track=[]
stem_colnames=[]
for name1 in bbecolnames_new:  #string operations getting rid of word after letter 
    word1 = stem.stem(name1)
    #stem_colnames.append(name1)
    for name2 in bbecolnames_new:
        word2 = stem.stem(name2)
        if (word1 == word2):
            stem_colnames.append(name2)
    word1=""
    word2=""
    stem_colnames
len(stem_colnames)   
stem_colnames
         
word_family = []                                        #########  STEMMING
i=0
while i <= len(colnames_new):
    name1 = colnames[i]
    stem1 = stem.stem(name1)
    word_family.append(stem1)
    i = i+1

colnames_new[0:25]
    
stem_colnames  
len(stem_colnames)                                    #########  STEMMING
len(colnames_new)
stemword_freqency = nltk.FreqDist(stem_colnames)
for key in stemword_freqency:
    if stemword_freqency[key] >5:
        print(key,stemword_freqency[key])

df_output = stemword_freqency.values

os.getcwd()
df_output = pd.DataFrame(corpusDF0) ## inspection
output_data = df_output  #output the total tweet datatable
output_data.to_csv("DTM_unnormalized_w_labels.csv", index=True)

######################## end k-means deatailed anlyais looksee
###############################################################################
######################################################
# CountVectorizers be set as 'content', 'file' or 'filename'
    #if set as 'filename' the **sequences passed as argument to fit**
    #is expected to be a list of filenames
    #https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#examples-using-sklearn-feature-extraction-text-countvectorizer

"""so this is wild! it is reading every file then smashing it into a dataframe!"""
myvect3 = CountVectorizer(input='filename')
    #CountVectorizer(analyzer='word', binary=False, decode_error='strict',
    #        dtype=<class 'numpy.int64'>, encoding='utf-8', input='filename',
    #        lowercase=True, max_df=1.0, max_features=None, min_df=1,
    #        ngram_range=(1, 1), preprocessor=None, stop_words=None,
    #        strip_accents=None, token_pattern='(?u)\\b\\w\\w+\\b',
    #        tokenizer=None, vocabulary=None)
x_dh = myvect3.fit_transform(listofcompletefilepaths) #vector w file names
x_dh.shape  ## documents by the total words
#print(x_dh) #now what do we have
    #  (0, 6387)     1           still not sure what this is!
    #  (0, 6056)     1

#get the feature names WHICH ARE THE WORDS!  
colnames_original = myvect3.get_feature_names()
print(colnames_original)
len(colnames_original)

#Create  a document term model - DTM ( a matrix of counts)
corpusDF0 = pd.DataFrame(x_dh.toarray(), columns=colnames_original) #ORIGINAL!!!!!!!!!!!!!!!!!!!!!!!!
corpusDF0.shape
#x1 = CountVectorizer.fit_transform(x_dh)
#corpusDF0 = pd.DataFrame(x_dh.toarray().transpose(),index =CountVectorizer.get_feature_names(colnames_original)) #,  columns=colnames_original)

print(corpusDF0)
corpusDF0.shape

#this dictionary is simply a numeric filename + generic numeric ID
mydict = {}  #now update the row names (corpus file names)
for i in range(0, len(listofjustfilenames)):
    mydict[i] = listofjustfilenames[i]
print(mydict)

#######################################################
############################ CREATING LABELS FOR TH3 DATA FRAME
############################
mylabels = []  #hand jam
mylabels= [1,1,1,1,1,1,1,1,1,2,2,1,2,2,2,2,2,2,2,2,3,3,1,3,3,3,3,3,3,3,3,1,1,1,1,1,1]
labels = pd.DataFrame(mylabels)
len(mylabels)
labels
corpusDF0
corpusDF0 = corpusDF0.rename(columns={'aaron':'labels'})
corpusDF0['labels'] = mylabels
corpusDF0
corpusDF0.shape

# so now have a doc train matrix - ------ create a training/test cube...
#buildthe corpus with teh papernames based on the file names

corpusDF0 = corpusDF0.rename(mydict, axis="index")  #index row names...
corpusDF0.shape
print(corpusDF0)

os.getcwd()
df_output = pd.DataFrame(corpusDF0) ## inspection
output_data = df_output  #output the total tweet datatable
output_data.to_csv("aBBE_today.csv", index=True)

############==> this is the BASE POINT FROM WHICH TO GO FORWARD
########################## >>>>> matrix needed for the k-means analysis
    #print(type(corpusDF0)) #check the type is a dataframe
    #mymatrix_data = corpusDF0.values
    #print(mymatrix_data)
#But first go on and remover stopwords and performing stemming
####################################################################
#REMOVE OUR OWN STOPWORDS - which are now residing in the columns
########################################################################

#BOUGHT PANDAS FOR EVERYBODY! TO LEARN THIS CODING!
corpusDF0['zeta'] # YES for accessing columns - still confused adding
    #the following loop is printing each column and all the values in it...
    #for name in columnnames3:
    #    print(corpusDF0[name])
#################========================================>REMVOE OWN STOPWRODS
#print("Initial column names: \n", columnnames3)
nostops = []
colnames_new = []   #build a new colmns list
for name in colnames_original:
    #print("FFFF",name)
    if((name in nostops) or (len(name)<3)):
        #print("word dropping: ",name)
        cleanDF = cleanDF.drop([name],axis=1) #cool drop stopword column
        #print(cleanDF)
    else:
        #I must add these new colnames
        colnames_new.append(name)

#################################### WITHOUT STOPWORDS
    
mystops = ["also","and","are","you","of","let","not","the","for","why","there","one","which","i"]

cleanDF = corpusDF0 #concept here make a cleanDF to add and remove columns
cleanDF.shape
colnames_new = []   #build a new colmns list
from nltk.tokenize import word_tokenize
stop_words=set(stopwords.words("english"))
for name in colnames_original:
    #print("FFFF",name)
    if((name in nostops) or (len(name)<=1)):
        #print("word dropping: ",name)
        cleanDF = cleanDF.drop([name],axis=1) #cool drop stopword column
        #print(cleanDF)
    else:
        colnames_new.append(name)
        
cleanDF        
cleanDF.shape       # Out[48]: (85, 8588) 
len(colnames_original) # origial import
len(colnames_new) #with stopwrods removed
colnames_new
#######################################################################
#(print("END\n",cleanDF))
#print("The ending column naes: \n",colnames)
""" so learning here the data is dirty and needs more cleaning bc white space
    so maybe need to use the read and write method to get workign correctly?
"""
###########################################################################
###  DR GATES CODE FOR USING STRING FUNCTIONS RIGHT STRIPPING BY A TEXT
###  VALUE. CAN BE USEFUL FOR PLURAL WORDS WITH "S" OR PERHAPS "E"
###  HAVE TO REALLY INSPECT THE WORDS AS SOME WORDS EMBEDDED IN OTHERS
##########################################################################
##########################################################################
## stringn function word stripping
# ---------------------------BBE ddint use for final project
##########################################################################
"""colnames is the new list after the stopwords have been removed  """
change_tracker=[]       
for name1 in colnames_new:  #string operations getting rid of word after letter 
    for name2 in colnames_new:  #on the right
        if (name1 == name2):
            #print("skip")
        elif(name1.rstrip("s") in name2): #thi sis good for plurals
            change_tracker.append(name1+ " " + name2)
            # like dog an dogs, but not for the hike an hiking
            #so I will srip and "e" if there is one...
            #print("combining:",name1, name2)
            #print(corpusDF0[name1])
            #print(corpusDF0[name2])
            #print(corpusDF0[name1] + corpusDF0[name2])
            #think about how to test this; at first you can do this
            #new = name1 + name2
            #cleanDF[new] = cleanDF[name1] + cleanDF[name2]
            #then before dropping any columns - print
            #the columns and their sum to check it
            cleanDF[name1] = cleanDF[name1] + cleanDF[name2]
            #later and once everything is test you will include this 
            #following line of code had commented out
            # "*****
            cleanDF = cleanDF.drop([name2], axis=1) #axis 1 is columns
change_tracker
len(change_tracker)
change_tracker
print(cleanDF.columns.values)

##############################################
#########  STEMMING - aborted for final DTM work
#########           ############################################
#from nltk.stem.wordnet import WordNetLemmatizer    
#lem = WordNetLemmatizer() #method we are using
#word = "flying"
#print("Lemmatized Word:",lem.lemmatize(word,"v"))  #v is for verb 
from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()        #print("Stemmed Word:",stem.stem(word))
change_tracker=[]

colnames_new[0:50] #list of words to debug this stemming...

word_family = []
skip_track=[]
stem_colnames=[]
for name1 in colnames_new:  #string operations getting rid of word after letter 
    word_family
    word1 = stem.stem(name1)
    stem_colnames.append(name1)
    for name2 in colnames_new:
        word2 = stem.stem(name2)
        if (word1 == word2):
            stem_colnames.append(name2)
            
word_family = []                                        #########  STEMMING
i=0
while i <= len(colnames_new):
    name1 = colnames[i]
    stem1 = stem.stem(name1)
    word_family.append(stem1)
    i = i+1

colnames_new[0:25]
    
stem_colnames  
len(stem_colnames)                                    #########  STEMMING
len(colnames_new)
stemword_freqency = nltk.FreqDist(stem_colnames)
for key in stemword_freqency:
    if stemword_freqency[key] >5:
        print(key,stemword_freqency[key])

df_output = stemword_freqency.values

df_output = pd.DataFrame(corpusDF0) ## inspection
output_data = df_output  #output the total tweet datatable
output_data.to_csv("aBBE_today.csv", index=True)

for name1 in colnames_new:  #string operations getting rid of word after letter 
    for name2 in colnames_new:  #on the right
        #if (name1 == name2): #if words equal at  start word position in loop
            #print("skip")
        if(stem.stem(name1) == stem.stem(name2)): #think should look for all subsequent 
            #change_tracker.append(name1+ " " + name2)
                                        #sten cases of same word
                                        #'abandon abandon',
                                        #'abandon abandoned',
                                        #'abandon abandoning',
            change_tracker.append(name1+ " " + name2)
            print("combining:",name1, name2)
            #print(corpusDF0[name1])
            #print(corpusDF0[name2])
            #print(corpusDF0[name1] + corpusDF0[name2])
            #think about how to test this; at first you can do this
            #new = name1 + name2
            #cleanDF[new] = cleanDF[name1] + cleanDF[name2]
            #then before dropping any columns - print
            #the columns and their sum to check it
            cleanDF[name1] = cleanDF[name1] + cleanDF[name2]
            #later and once everything is test you will include this 
            #following line of code had commented out
            # "*****
            cleanDF = cleanDF.drop([name2], axis=1) #axis 1 is columns
change_tracker           
cleanDF.shape
len(colnames_new)
cleanDF

####################################
#############################################################
"""  SO NEED TO WORK HERE ON ADDING THE DOCUMENTS TO THE FRAME BUT MOVING ON.."""
cleanDF
testDF= cleanDF
##add labels back into the dataframe
testDF = documents.to_frame() #index to 0  #thi sis interesting!
print(type(documents))
testDF.index = documents.index - 1
#print(new_labels)
labeledclean_DF["Label"] = new_labels ##  NOW MAKE THE FINALIZED DATA FRAME

#############################################################
### NORMALIZATION
###############################################################
###############################################################
"""##################### TF-IDF  """ #Normalization
###############################################
####################################didt do any stemmiong noting
corpusDF0
cleanDF = corpusDF0  #connect back to data
df_much_ado = bbecorpusDF0  #much ado
df_much_ado_no_stops =bbecleanDF
import math

df_data = pd.DataFrame(df_much_ado_no_stops).values.astype(int)
df_data
#transpose the frame
df_data_transposed = df_data.T  #transpose the frame
df_data_transposed[0]
df_data_transposed.shape[1] ## of words transposed, want 1 for docs

mydocfreq=[]   #word counts across the documents
for x in range(0,len(df_data_transposed)):
    wf = int(sum(df_data_transposed[x])) #[x]
    idf = wf / df_data_transposed.shape[1]  #number of docs
    mydocfreq.append(idf)
    wf=""
    idf = ""

df_mydocfreq_inverse = pd.DataFrame(mydocfreq).values.astype(float)
df_mydocfreq = pd.DataFrame(df_mydocfreq_inverse).T  #thats right make 1 x 1384
df_mydocfreq
df_tfidf = pd.DataFrame(df_data).values.astype(float) #build frame
df_tfidf.shape
#zero out the dataframe - I DOULBLe checked this owrking
for x in range(0,len(df_tfidf)): # 
    y=0
    #demoninator = float(df_mytotalword_perdoc[x])
    while y <= (df_tfidf.shape[1]-1):  #shape gives the y dimension of columns
        df_tfidf[x,y] = 0
        y +=1
#####===> TF-IDF the data
for x in range(0,len(df_data)): # rows in data frame
    y=0
    while y <= (df_tfidf.shape[1]-1):  #shape gives the y dimension of columns
        df_tfidf[x,y] = df_data[x,y]* math.log(mydocfreq[y]) 
        y +=1 
df_tfidf.shape
len(colnames_new)

#---------------------------------------------------model 1 here
#export back to Excel
DF_Homework = pd.DataFrame(df_tfidf)
output_data = DF_Homework  #output the total tweet datatable
output_data.to_csv("much_ado.csv", index=True)
df_much_ado = df_tfidf
df_much_ado.shape
labeledclean_DF =pd.DataFrame(df_tfidf)
labeledclean_DF.shape
len(bbecolnames_new)
        #new_labels = mylabel.to_frame() #index to 0  #thi sis interesting!
        ##print(type(new_labels))
        #new_labels.index = new_labels.index - 1
        ##print(new_labels)
        ###  NOW MAKE THE FINALIZED DATA FRAME
        #labeledclean_DF["Label"] = new_labels  #add new label tot he dataframe
        #print(labeledclean_DF)
#########################################################
#######NEED MATRIX DATA ################# CLUSTERING   #######################
#########################################################
labeledclean_DF  #the label is in the index brian
from sklearn.cluster import KMeans#Using SKlearn - - WOWSERS IS THSI FAST...
import numpy as np #kmeans_object = sklearn.cluster.KMeans(n_clusters=3)
#print(kmeans_object)
    #KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    #    n_clusters=3, n_init=10, n_jobs=None, precompute_distances='auto',
    #    random_state=None, tol=0.0001, verbose=0)
labeledclean_DF.values   #K-means model
mymatrix_data = labeledclean_DF.values #matrix of k-means data
kmeans_object = KMeans(n_clusters=5)   #tyring 3 and 4 clusters
kmeans_object.fit(mymatrix_data)       #fit model

kmeanslabels = kmeans_object.labels_   #get cluster assignment labels
len(kmeanslabels)  #yup 55 chracters
labeledclean_DF

#Build Results
df_output = pd.DataFrame(labels) ## inspection
output_data = df_output  #output the total tweet datatable
output_data.to_csv("w_stopwords_labels_much_ado_final.csv", index=True)
################################
######################
###############
# ths is working..... FOR FINAL PRJOECT AND HOPE YOU CAN SLEEP AGAIN
myresults = pd.DataFrame([corpusDF0.index,labels]).T #format results as DF
myresults   #ok so this is who speaks most similar in the play
import matplotlib.pyplot as plt
plt.plot(myresults[0],myresults[1],'o')

df_output = pd.DataFrame(myresults) ## inspection
output_data = df_output  #output the total tweet datatable
output_data.to_csv("aBBE_today.csv", index=True)

myresults = myresults.rename(mydict, axis="index")    #add column to merge
myresults
myresults = myresults.rename(columns={1:'k-means-label'}) #renaming
myresults = myresults.rename(columns={0:'docname'})
myresults.head()
documents = pd.DataFrame(doc) #original list of the documents from import
documents = pd.DataFrame([corpusDF0.index,labels]).T #add column to merge
documents = documents.rename(columns={1:'authorID'})  #renaming
documents = documents.rename(columns={0:'docname'})
documents.head()
#Merge the results
finalDF = myresults.merge(documents, on='docname')  #yippeeeeeeeee  !!!!
finalDF
from pandas_ml import ConfusionMatrix
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
y_actual=[]
y_predict=[]
y = finalDF.columns.get_loc("authorID") #get column index
y1 = finalDF.columns.get_loc("k-means-label")
y
for x in range(0,len(finalDF)):
    y_actual.append(finalDF.iat[x,y])
    y_predict.append(finalDF.iat[x,y])
y_actual

confusion_matrix = confusion_matrix(y_actual,y_predict)
confusion_matrix

import seaborn as sn
import matplotlib.pyplot as plt
df_cm = pd.DataFrame(confusion_matrix, range(4),range(4))
sn.set(font_scale=1.4)
sn.heatmap(df_cm,annot=True,annot_kws={"size":16}) #font size

#############################  END CLUSTERING   ########################
#############################  END CLUSTERING   ########################
#############################  END CLUSTERING   ########################
#############################  END CLUSTERING   ########################
#############################  END CLUSTERING   ########################

#preprocessin and categorization
len(corpusDF0)

""" so need to better understand what going on with word frequency down here
was able to figure out hte next day and make the word cloud!!!
read -> clean -> vectorize -> stopwords"""
###################################################################
## CONNECTING TO BUILD WORD FREQUENCY AND WORDCLOUDS from Week 2
###################################################################

#data from the WAY top
mycorpus_data = corpusDF0
wordlist = [] ##what is happening here is joining all the lines read in
              ##, joining it all today
wordlist = " ".join(mycorpus_data) 
wordlist
tokenized_word=word_tokenize(wordlist)
len(tokenized_word)
tokenized_word
stop_words=set(stopwords.words("english"))
corpus_no_stopwords=[]
for w in tokenized_word:
    if w not in stop_words:
        corpus_no_stopwords.append(w)
#==> 3) word Frequency
len(corpus_no_stopwords)
corpus_no_stopwords

import re  #now perform more cleaning
mystops = ["also","and","are","you","of","let","not","the","for","why","there","one","which"]
newlist = []
for word in corpus_no_stopwords:
    #print("the new word is: ",word)
    #placeinoutputfile = "The next word before is: " + word + "\n"
    #OUTFILE.write(placeinoutputfile)
    word = word.lower()
    word = word.lstrip()
    word = word.strip("\n")
    word = word.strip("\\n")
    word = word.replace(",","")
    word = word.replace(" ","")
    word = word.replace("_","")
    word = re.sub('\+', '',word)
    word = re.sub('.*\+\n','',word)   ##LOOKS FUNNY! single quotes!
    word = re.sub('zz+','',word)
    word = word.replace("\t","")
    word = word.replace(".","")
    word = word.replace("\'s","")  #was comment3d out
    word = word.strip()
    ##word.replace("\","")  #was commented out
    #if((name in mystops) or (len(name)<3)):
    if ((word not in["","\\","'","*",":",";"]) or (word not in mystops)):
        if len(word) >=3:
            if not re.search(r'\d',word): ##remove the digits
                # HW2 ===non english words
                newlist.append(word)
                #placeinoutputfil = "The next word AFTER is: " + word + "\n"
                #OUTFILE.write(placeinoutputfile)
len(corpus_no_stopwords)
newlist = corpus_no_stopwords   #makesgut to get running wo stopwords
len(newlist)
newlist

mostfrequentwords = nltk.FreqDist(newlist)
mostfrequentwords
top_words=mostfrequentwords.most_common(200) #words used most in the tweets
DF_topwords = pd.DataFrame(top_words)
print("....50 Top Words from Tweets. \n",DF_topwords)
top_words
wordcloud_items=[] #make a dictionary  ====>move to dictionary in future
for word, freq in top_words:   #print the most commone words
        print("Word:",word,freq)
        wordcloud_items.append(word)
print(wordcloud_items)
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
wordcloud_items = " ".join(wordcloud_items)  ##  join
print(wordcloud_items)  # lower max_font_size, change the maximum number of word and 
wordcloud = WordCloud(max_font_size=50, max_words=80, background_color="white").generate(wordcloud_items)

wordcloud.random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

#NOW DOULB CHECK THE TOTALWORDS
mycountvect = CountVectorizer (input = "content")  #this uses a list!!!
CV = mycountvect.fit_transform(newlist)
mycountvect.get_feature_names()
mycolumnnames = mycountvect.get_feature_names()
vectorizedDF_text = pd.DataFrame(CV.toarray(),columns=mycolumnnames)
len(mycolumnnames)

is to build a wordcloiud of frequency
df_data = pd.DataFrame(corpusDF0).values.astype(int)
mytotalword_perdoc=[]   #get tyhe total counts for normalization
for x in range(0,len(df_data)):
    total = int(sum(df_data[x]))
    mytotalword_perdoc.append(total)
df_mytotalword_perdoc = pd.DataFrame(mytotalword_perdoc).values.astype(int)
df_mytotalword_perdoc[1:4]

###########################################
###################
#==> VISUSLIZING DISTANCES
###############################################
######################################################################
# AN OPTION IS ASSIGN A POINT ON A PLANTE TO EACH TEXT THAT THE THE DISNTANCE
#hbetween the points is proportional to the pairwaied euclidence or costin
#this typ eof visualized is called multidomensional scaling (MDS) in scikit-learn

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import ward, dendrogram

#get the data
vectorizer = CountVectorizer(min_df=1, ngram_range=(1,2), token_pattern=r'\b\w+\b')
# corpus = ['doc-1','doc-2'...]

listofcompletefilepaths   #this is from above pulling ion the shakespear data

#-----------------------------------so I can vectorizer
vectorizer = CountVectorizer(input='filename')
dtm = vectorizer.fit_transform(listofcompletefilepaths)
dtm.shape
print(type(dtm))
#vocab is a list
vocab = vectorizer.get_feature_names() # change to a list
######################################--------------here are my lables
vocab.dtype()
DT_vocab = vocab
DT_vocab.remove('label')
len(DT_vocab)

dtm = dtm.toarray() #convert to regular array
dtm.shape
# waqys to count the word :anythong" in first file on the list of files
print(list(vocab))

#----------------------------------wordclouds
# DTM wordclouds ###########################################
#----------------------------------------------------working to here
What I what here is the highest frequency word for 37 total plays.....__class__

comedy_1 =[]
comedy_2=[]
mycorpus_data
wordlist = [] ##what is happening here is joining all the lines read in
              ##, joining it all today
wordlist = " ".join(dtm) 
wordlist
tokenized_word=word_tokenize(wordlist)
len(tokenized_word)
tokenized_word
stop_words=set(stopwords.words("english"))
corpus_no_stopwords=[]
for w in tokenized_word:
    if w not in stop_words:
        corpus_no_stopwords.append(w)
#==> 3) word Frequency
len(corpus_no_stopwords)
corpus_no_stopwords

anthony_idx = list(vocab).index('bleed')
print(anthony_idx)
print(list(vocab)[500:550])
print(dtm[500:520,500:520])
dtm.shape
#---------------------------------
#create a table of word count to compare one to another 
# so in this case I have 37 plays.........................................

columns = ["playname","bleed","blessed","nothing"]
mylist1 =["bleed"]
mylist2 = ["blessed"]
mylist3 = ["nothing"]
for someword in ["bleed","blessed","nothing"]:
    anthonyword = (dtm[0,list(vocab).index(someword)])
    mylist1.append(anthonyword)
    blessword = (dtm[0,list(vocab).index(someword)])
    mylist2.append(blessword)
print(mylist1)
print(mylist2)
#---------------------------------------
##############################################################
#########################################
##########################
#################    BULDING TRAINIG AND TEST DATA FRAMES
#################################
#######################################################
#######################################################################
#    hogna 515 you are comparing books - you have buyildt corpus DF0
#no stopwords
corpusDF0
trainDF = pd.DataFrame ##################  build the training and test
testDF = pd.DataFrame
trainDF = corpusDF0.iloc[[0,1,2,3,4,5,6,7,8,9,10,11,12,17,18,19,20,21,22,23,24,27,28,29,30,31,32,33,34]]
testDF = corpusDF0.iloc[[13,14,15,16,25,26,35,36]]
trainDF.shape
testDF.shape

mytrainlabels = trainDF['labels']
mytestlabels = testDF['labels']
mytrainlabels
mytestlabels

trainDF = trainDF.drop(['labels'], axis=1)
testDF = testDF.drop(['labels'], axis=1)

###############################################################
"""##################### TF-IDF  """ #Normalization
#########################################################################
import math
df_data = pd.DataFrame(trainDF).values.astype(int)
#-------------------------thse are run seperately!
df_data = pd.DataFrame(testDF).values.astype(int)
#--------------------------------------------------
df_data.shape
#transpose the frame
df_data_transposed = df_data.T  #transpose the frame
df_data_transposed[0]
df_data_transposed.shape[1] ## of words transposed, want 1 for docs

mydocfreq=[]   #word counts across the documents
for x in range(0,len(df_data_transposed)):
    wf = int(sum(df_data_transposed[x])) #[x]
    idf = wf / df_data_transposed.shape[1]  #number of docs
    mydocfreq.append(idf)
    wf=""
    idf = ""

df_mydocfreq_inverse = pd.DataFrame(mydocfreq).values.astype(float)
df_mydocfreq = pd.DataFrame(df_mydocfreq_inverse).T  #thats right make 1 x 1384
df_mydocfreq.shape

df_tfidf = pd.DataFrame(df_data).values.astype(float) #build frame
df_tfidf.shape
#zero out the dataframe - I DOULBLe checked this owrking
for x in range(0,len(df_tfidf)): # 
    y=0
    #demoninator = float(df_mytotalword_perdoc[x])
    while y <= (df_tfidf.shape[1]-1):  #shape gives the y dimension of columns
        df_tfidf[x,y] = 0
        y +=1
#####===> TF-IDF the data
for x in range(0,len(df_data)): # rows in data frame
    y=0
    while y <= (df_tfidf.shape[1]-1):  #shape gives the y dimension of columns
        #df_tfidf[x,y] = df_data[x,y]* math.log(df_mydocfreq[y])
        try:
            df_tfidf[x,y] = df_data[x,y]* math.log(df_mydocfreq[y])
        except:
            df_tfidf[x,y] = 0
        y +=1 
df_tfidf
df_tfidf.shape
#export back to Excel
df_output = pd.DataFrame(df_tfidf)
df_output
output_data = df_output  #output the total tweet datatable
output_data.to_csv("hoemrun.csv", index=True)
#----------------------------------------------------------
trainDFn = df_tfidf
train_bigdata_backup = df_tfidf
testDFn =df_tfidf
test_bigdata_backup = df_tfidf

os.getcwd()
df_output = pd.DataFrame(testDFn)
df_output.to_csv("testDFn.csv", index=True)
#assign the labels back
############################
################################### HOGANS SVM THAT IS WORKIGN......
#############################################################
######################## workingt                 svm
################################################
#-------------------------------SVM ----hogan this was manual way
#SVM MODEL 1
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
svm_model = LinearSVC(C=10, max_iter=3000)
svm_model.fit(trainDFn, mytrainlabels)
print("SVM prediction:\n", svm_model.predict(testDFn))
print("actual:", mytestlabels)
print(mytestlabels)
svm_matrix = confusion_matrix(mytestlabels, svm_model.predict(testDFn))
print(svm_matrix)
#Better confusion matrix heatmap
import seaborn as sn  
mytestlabels
data = {'y_predict' : [2,2,3,2,1,3,1,3], 'y_actual' : [2,2,2,2,3,3,1,1], 'play_id' : [21,22,23,24,32,33,8,9 ]}
df = pd.DataFrame(data, columns=['y_actual','y_predict', 'play_id'])
print(df)
confusion_matrix = pd.crosstab(df['y_actual'], df['y_predict'],rownames = ['Actual'], colnames=['Predicted'])
sn.heatmap(confusion_matrix, annot=True)
from sklearn.metrics import accuracy_score
accuracy_score(df['y_actual'], df['y_predict'])
#----------------------------------------2ND VERIONS
#SVM MODEL 2
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
svm_model = LinearSVC(C=7, max_iter=30000, random_state=1)  #no change!
svm_model.fit(trainDFn, mytrainlabels)
print("SVM prediction:\n", svm_model.predict(testDFn))
print("actual:", mytestlabels)
print(mytestlabels)
2svm_matrix = confusion_matrix(mytestlabels, svm_model.predict(testDFn))
print(2svm_matrix)
#Better confusion matrix heatmap
import seaborn as sn  # ----------------done manually to create heatmapo
mytestlabels
data = {'y_predict' : [2,2,3,2,1,3,1,3], 'y_actual' : [2,2,2,2,3,3,1,1], 'play_id' : [21,22,23,24,32,33,8,9 ]}
df = pd.DataFrame(data, columns=['y_actual','y_predict', 'play_id'])
print(df)
confusion_matrix = pd.crosstab(df['y_actual'], df['y_predict'],rownames = ['Actual'], colnames=['Predicted'])
sn.heatmap(confusion_matrix, annot=True)
from sklearn.metrics import accuracy_score
accuracy_score(df['y_actual'], df['y_predict'])

############################
###############################################
#############################################################

####################################
#############################################################
#--------------------------------------------- decision tree
#############################################################################
import sklearn.datasets as datasets
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals.six import StringIO  
from IPython.display import Image    
from sklearn.tree import export_graphviz
import pydotplus as pydot
d9f=pd.DataFrame(trainDFn, mytrainlabels) #your training and labels
#graphing from: https://stackoverflow.com/questions/31209016/python-pydot-and-decisiontree
clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100,
                                  max_depth=3, min_samples_leaf=5)
clf_gini = DecisionTreeClassifier(criterion="gini", random_state=1000,
                                  max_depth=30, min_samples_leaf=30)
clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=100,
                                  max_depth=3, min_samples_leaf=5)
clf_entropy_4 = DecisionTreeClassifier(criterion="entropy", random_state=100,
                                  max_depth=100, min_samples_leaf=15)
clf_gini.fit(trainDFn, mytrainlabels) #-------------------> runs
clf_entropy.fit(trainDFn, mytrainlabels) 
clf_entropy_4.fit(trainDFn, mytrainlabels) 

        #dtree=DecisionTreeClassifier()
        #dtree.fit(d9f,y)
#------------------------------graphing code
dot_data = StringIO()
#'-this does not always building in python
    #graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) #this now workiing
    #Image(graph.create_png())
#-----------------------------------------------workaround
#this code creates a .dot file
    #######################################################################
#---version a
tree.export_graphviz(dtree, out_file=dot_data, feature_names=DT_vocab)
export_graphviz(dtree, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
tree.export_graphviz(clf_gini, out_file=dot_data, feature_names=DT_vocab)
graph = pydot.graph_from_dot_data(dot_data.getvalue())  
tree.export_graphviz(dtree, out_file='b_DT_treepic.dot', feature_names=DT_vocab)
#---b (same outcomes)
export_graphviz(clf_gini, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
tree.export_graphviz(clf_gini, out_file=dot_data, feature_names=DT_vocab)
graph = pydot.graph_from_dot_data(dot_data.getvalue())  
tree.export_graphviz(dtree, out_file='b_DT_treepic.dot', feature_names=DT_vocab)
#----c - entropy
export_graphviz(clf_entropy, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
tree.export_graphviz(clf_entropy, out_file=dot_data, feature_names=DT_vocab)
graph = pydot.graph_from_dot_data(dot_data.getvalue())  
tree.export_graphviz(dtree, out_file='c_DT_treepic.dot', feature_names=DT_vocab)
#---4 other - trying to get a wide tree
export_graphviz(clf_entropy_4, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
tree.export_graphviz(clf_entropy_4, out_file=dot_data, feature_names=DT_vocab)
graph = pydot.graph_from_dot_data(dot_data.getvalue())  
tree.export_graphviz(dtree, out_file='d_DT_treepic.dot', feature_names=DT_vocab)
#on anconda prompt - have to run to open these files
a) dot -T png treepic.dot -o treepic.png
b) dot -T png b_DT_treepic.dot -o b_DT_treepic.png
c) dot -T png c_DT_treepic.dot -o c_DT_treepic.png
d) dot -T png d_DT_treepic.dot -o d_DT_treepic.png


Image(graph.create_png()) 
#use this cfrom command line
os.getcwd() #know whwere file is an on command prompt
command promotpt type cd "Arthur\Text_Mining\Data" #change for right folder
#on the anaconda command type
#============>       dot -T png treepic.dot -o treepic.png
#ANACONDA
"""(base) C:\Users\BBE>cd "c:\\Users\BBE\BBE\DATA\myCorpus"
(base) c:\Users\BBE\BBE\DATA\myCorpus>dot -T png treepic.dot -o treepic.png"""




print(graph)

#graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
#-------------------------------------learnigns
print(clf_gini)
print("Accuracy is ", accuracy_score(y_test,y_pred)*100)
#########################
##############################################  end svm
mytrainlabels
mytestlabels
df_train_labels = pd.DataFrame(mytrainlabels)
df_train_labels

df_output = pd.DataFrame(mytrainlabels)
output_data = df_output  #output the total tweet datatable
output_data.to_csv("train_labels.csv", index=True)

trainDF['labels']=mytrainlabels
testDF['labels']=mytestlabels 

df2 = pd.DataFrame([columns,mylist1, mylist2])
print(df2)

#------------COMPARINGN BOOKS
######################################### ward cosince similarity
#each row the document term matrix
#matrix dtm is a swequesnce of the novels word frequences
#get the euclidenan idstation btween novels usein skealrn
dtm.shape
dist = euclidean_distances(dtm)
print(np.round(dist,0))  #dist betweeen emall and prices is 3846
#measues of the distance that takes into account the length of the document
#called cosine similarity
cosdist = 1 - cosine_similarity(dtm)
print(np.round(cosdist,3))
cosdist.shape
# visualizing distances
# an option for visualizing distances is to assign a point on a plance
# to each text such tht hte distance betgweens poitns is proporotional
#to the pairwise ecuilidand or cosing distatnces
#this type of visaulize is called multidemtnionall scaling(MDS)
#in scikit-learn and R called mdscale

          ## precomputr meands we will give the dist (as cosine sim
mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state=1)
pos = mds.fit_transform(cosdist) # shape(n_components, featuren_samples)
pos  #this is what I want
#stuck wont transformf
----------------------------------------------
plt.plot(pos[0],pos[1])  this workds


#we are now here on the nanmes....................................
###################################
########################################################################
names = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37']
xs, ys = (pos[:,0],pos[:,1]) 
for x, y, name in zip (xs, ys, names):              #this is working
    plt.scatter(x,y)
    plt.text(x,y,name)
plt.show() 

#plotting distancwe in 3D - multi-dimension scaling
mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state=1)
pos = mds.fit_transform(cosdist)
pos
pos.shape
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  #3d
#ax.scatter(pos[:0],pos[:,1],pos[:,2])
#for x,y,z,s in zip(pos[:0],pos[:1],pos[:,2],names):
#    ax.text(x,y,z,s)
#----------------------------------------------
ax.scatter(pos[:0],pos[:,1])
for x,y in zip(pos[:0],pos[:1],names):
    ax.text(x,y)
#---------------------------------------------
ax.set_xlim3d(-.05,.07)
ax.set_ylim3d(-.008,.008)
ax.set_zlim3d(-.05,.05)
plt.show() #------------------------------not working

#-------------------------------alternative as not working
#################################               this is wsorking!!!!!!!
names  #this is names of the plays
linkage_matrix = ward(cosdist)
fig,ax = plt.subplots(figsize = (15,20))
ax = dendrogram(linkage_matrix, orientation='right',labels=names)

plt.tick_params(\
                axis = 'x',
                which ='both',
                bottom = 'off',
                top = 'off',
                labelbottom = 'off')
plt.tight_layout()

    #########################################################################
"""more wordclound code """
## building a whole list of the all the words for a wordcloud on bottom
## reads in all the lines! then vectorize them for wordcloud
"""WORD CLOUD CODE JUMPS DOWN TO THE BOTTOM"""
#######################################################################
listofjustfilenames[1]
#check if the file is a csv or a txt file....
mycorpus_data=[]
for i in range(0,len(listofjustfilenames)):
    #filename = open(listofjustfilenames[i] + ".txt","r")   #txt or csv
    filename = open(listofjustfilenames[i] + ".txt" ,"r")   #txt or csv
    for line in filename:
        textline = line.strip()
        mycorpus_data.append(textline)   #well this is brinig in every line.
    filename.close()
len(mycorpus_data)
mycorpus_data
#inspecting file names in excel to make s graph
df_output = pd.DataFrame(mycorpus_data)
output_data = df_output  #output the total tweet datatable
output_data.to_csv("aShakespeare.csv", index=True)

##########################################################################
#######################               SVM w cross validation
#                              diddnt use
###########################################################################

###################################################################
##########   SVM ----------------------- SVM
##################################################################
from sklearn.model_selection import train_test_split

dfnormalized2['Label']=mylabels
dfnormalized2['Label']=mylabelsB  #Ebinary
dfnormalized2

print(m2_X_train_vec[0].toarray())

y=train['Character'].values  #LABLES --- Sentiment
X=train['Phrase'].values
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.4)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
X_train

#CREATE TRAINING AND TEST DATA SET splitting & test_size paramter DR Gates
trainDF, testDF = train_test_split(dfnormalized2, test_size=0.4)
trainDF.shape
testDF.shape
trainDF
testDF.head() 

m2_X_train_vec
m2_X_test_vec

from sklearn.svm import LinearSVC
SVM_model = LinearSVC(C=10)
SVM_model.fit(m2_X_train_vec, trainlabels)
#BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
print("SVM prediction:\n", SVM_Model.predict(testDF))
print("actual: ")
print(testlabels)

#CROSS VALIDATION---------------I DONT REALLY REMEMBER HOW TO INTERPRET...
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
nb_clf_pipe = Pipeline([('vect',CountVectorizer(encoding='latin-1',binary=False)),('nb', MultinomialNB())])
scores = cross_val_score(nb_clf_pipe, X, y, cv=3)
mNB_avg=sum(scores)/len(scores)
print(mNB_avg)

#CROSS VALIDATION
nb_clf_pipe = Pipeline([('vect',CountVectorizer(encoding='latin-1',binary=True)),('nb', MultinomialNB())])
scores = cross_val_score(nb_clf_pipe, X, y, cv=3)
Bernoulli_avg=sum(scores)/len(scores)
print(Bernoulli_avg)

###################################
####################################################
##############################################################wingt an a praryer
"""Created on Thu Aug 29 14:35:09 2019
@author: Brian Hogan
Purpose: ist736 Homework 7
"""
"""Created on Thu Aug 29 14:35:09 2019
@author: Brian Hogan
Purpose: ist736 Homework 7
"""
import os
import re
import nltk
import pandas as pd
import numpy as np
import sklearn
import string
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import matplotlib.pyplot as plt  #learnign dataframe
###########################################################
"""other team members did this so i didn't use"""
#########################################################################
##########################  NAIVE BAYNES  ###############################
#########################################################################
###################################################################
##########   CREATING TRAINING AND TEST DATA SETS
##################################################################
#Create the testing set - grab sample from the training set.
#Be careful. Notice that right now our trianing set is sorted by label
#if you train set is large enough, you can take a random sample
from sklearn.model_selection import train_test_split
#add the labels back in before splitting the data set
dfnormalized2['Label']=mylabels
dfnormalized2['Label']=mylabelsB  #Ebinary
dfnormalized2

trainDFn
testDFn
mytrainlabels
mytestlabels

#CREATE TRAINING AND TEST DATA SET splitting & test_size paramter DR Gates
trainDF, testDF = train_test_split(trainDFn, test_size=0.4)
trainDF.shape
testDF.shape
trainDF
testDF.head()     
###################################################################
##########   NAIVE BAYNES
#https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB.fit
##look up this model you learn that it wasnt the df seperate from labels 
##################################################################
## SAVE LABELS  ##IMPORTANT - CAN NOT LEAVE LABELS ON THE TEST SET
trainlabels = trainDF['Label']   
testlabels = testDF['Label']      
trainDF_nolabels = trainDF.drop(['Label'], axis=1)
testDF = testDF.drop(["Label"], axis=1)
testDF.head()
trainDF_nolabels.head()
trainDF_nolabels.shape
from sklearn.naive_bayes import MultinomialNB
mymodelNB = MultinomialNB()   
mymodelNB.fit(trainDF_nolabels, trainlabels)
# yoooo hogan
mymodelNB.fit(trainDFn, mytrainlabels)
mymodelNB.fit(trainDF_nolabels, trainlabels)  #all labels need to be same
prediction = mymodelNB.predict(testDF)
#print("The prediction from NB is :")
print(prediction)
#print("the actual labels are:")
label_print=[]
for label in testlabels:
    label_print.append(label)
print(label_print)
from sklearn.metrics import confusion_matrix
cnf_matrix = confusion_matrix(testlabels, prediction)
print("the confusion matrix is: ")
print(cnf_matrix)
print(np.round(mymodelNB.predict_proba(testDF),2))
## conTfusion matrix
#the confusion matrix is square and is labels x labels
#we have 2 labels so ours will be 2x2
#the matrix :
#  rows are the true labels
#  columns are the predicted
#  it is alphabeitcal & the numbers are how many

##preduction probabilities
##columns are the labels in alphabetical order
##the decimal in the matrix are th prob of being that label

###################################################################
##########   Bernoulli       using the Binary
##################################################################
# DF is not correct - be sure to fix it - ONLY BINARY
from sklearn.naive_bayes import BernoulliNB
bernmodel = BernoulliNB()
bernmodel.fit(trainDF_nolabels, trainlabels)
#BernoulliNB(alpha=1.0, binarize=0.0, class_prior = None, fit_prior=True)
print("Bernoulli prediction: \n", bernmodel.predict(testDF))
print("actual: ")
print(testlabels)
######################
##########################
###################################################################
##########   SVM ----------------------- SVM
##################################################################
dfnormalized2['Label']=mylabels
dfnormalized2['Label']=mylabelsB  #Ebinary
dfnormalized2

print(m2_X_train_vec[0].toarray())

y=train['Character'].values  #LABLES --- Sentiment
X=train['Phrase'].values
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.4)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
X_train

#CREATE TRAINING AND TEST DATA SET splitting & test_size paramter DR Gates
trainDF, testDF = train_test_split(dfnormalized2, test_size=0.4)
trainDF.shape
testDF.shape
trainDF
testDF.head() 
mytrainlabels
m2_X_train_vec
m2_X_test_vec

from sklearn.svm import LinearSVC
SVM_model = LinearSVC(C=10)
SVM_model.fit(m2_X_train_vec, trainlabels)
#BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
print("SVM prediction:\n", SVM_Model.predict(testDF))
print("actual: ")
print(testlabels)

#CROSS VALIDATION---------------I DONT REALLY REMEMBER HOW TO INTERPRET...
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
nb_clf_pipe = Pipeline([('vect',CountVectorizer(encoding='latin-1',binary=False)),('nb', MultinomialNB())])
scores = cross_val_score(nb_clf_pipe, X, y, cv=3)
mNB_avg=sum(scores)/len(scores)
print(mNB_avg)

#CROSS VALIDATION
nb_clf_pipe = Pipeline([('vect',CountVectorizer(encoding='latin-1',binary=True)),('nb', MultinomialNB())])
scores = cross_val_score(nb_clf_pipe, X, y, cv=3)
Bernoulli_avg=sum(scores)/len(scores)
print(Bernoulli_avg)

##############################  ARTHUS QUESTIONS ON GETTING A GRID TO WORK
#----------------------------- team mate questions
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)
iris = load_iris()
cross_val_score(clf, iris.data, iris.target, cv=10)
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(iris.data, iris.target)
clf = clf.fit(iris.data, iris.target)   # workings
#----------------------------- works to here

#---------------------------------------------

######################################
################################
############## arthus grid view
print(__doc__)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Parameters
n_classes = 3
plot_colors = "ryb"
plot_step = 0.02
# Load data
iris = load_iris() #------------------visualizatiobn for cluster groups
for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
                                [1, 2], [1, 3], [2, 3]]):
    # We only take the two corresponding features
    X = iris.data[:, pair]
    y = iris.target
    X = trainDF.data
    y = testDF.data

    # Train
    clf = DecisionTreeClassifier().fit(X, y)

    # Plot the decision boundary
    plt.subplot(2, 3, pairidx + 1)

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))
    plt.tight_layout(h_pad=0.5, w_pad=0.5, pad=2.5)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)

    plt.xlabel(iris.feature_names[pair[0]])
    plt.ylabel(iris.feature_names[pair[1]])

    # Plot the training points
    for i, color in zip(range(n_classes), plot_colors):
        idx = np.where(y == i)
        plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                    cmap=plt.cm.RdYlBu, edgecolor='black', s=15)

plt.suptitle("Decision surface of a decision tree using paired features")
plt.legend(loc='lower right', borderpad=0, handletextpad=0)
plt.axis("tight")
plt.figure()
clf = DecisionTreeClassifier().fit(iris.data, iris.target)
plot_tree(clf, filled=True)
plt.show()

#------------hogan decision gtree
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,
                               max_depth=3, min_samples_leaf=5)
clf_gini.fit(X_train, y_train)
clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
max_depth=3, min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)
y_pred = clf_gini.predict(X_test)
y_pred
print "Accuracy is ", accuracy_score(y_test,y_pred)*100

#----------------------------------------
--- bbe  experimenting with arthus grid matrix

######################################
################################
############## arthus grid view
print(__doc__)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Parameters
n_classes = 3
plot_colors = "ryb"
plot_step = 0.02
# Load data
iris = load_iris() #------------------visualizatiobn for cluster groups
iris
xx.ravel()
np.c_[xx.ravel(), yy.ravel()]
trainDF

import numpy as np
trainDF2 = trainDFn
trainDFn.to_numpy()

testDF2 =testDFn.to_numpy(copy=True)

for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
                                [1, 2], [1, 3], [2, 3]]):
    # We only take the two corresponding features
#    X = iris.data[:, pair]
#    y = iris.target
    X = trainDF
    y = testDF
    # Train
    clf = DecisionTreeClassifier().fit(X, y)
    # Plot the decision boundary
    plt.subplot(2, 3, pairidx + 1)
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))
    plt.tight_layout(h_pad=0.5, w_pad=0.5, pad=2.5)
    #Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#    Z = Z.reshape(xx.shape)
#    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)
    Z = clf.predict(y, mytrainlabels)
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)
    
    plt.xlabel(mytrainlabels[pair[0]])
    plt.ylabel(ytestlabels[pair[1]])
    # Plot the training points
    for i, color in zip(range(n_classes), plot_colors):
        idx = np.where(y == i)
        plt.scatter(X[idx, 0], X[idx, 1], c=color, label=mytestlabels,
                    cmap=plt.cm.RdYlBu, edgecolor='black', s=15)
len(mytestlabels)
len(mytrainlabels)
plt.suptitle("Decision surface of a decision tree using paired features")
plt.legend(loc='lower right', borderpad=0, handletextpad=0)
plt.axis("tight")
plt.figure()
clf = DecisionTreeClassifier().fit(iris.data, iris.target)
plot_tree(clf, filled=True)
plt.show()