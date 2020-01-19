# credit: Eric Cornforth, Felipe Galindo

class keywords:
    #initialization
    def __init__(self, name):
        self.name = name
        self.keyExists = True
    #setters
    def setKeyExists(self, keyExists, yes):
        self.keyExists = yes

    #getters
    def getName(self):
        return self.name
    
    def getExistence(self):
        return self.keyExists

class badWords:
    def __init__(self, name):
        self.name = name
        self.exists = False

    #getters
    def getName(self):
       return self.name


#arrayOfKeywords: items to be checked
#arrayOfBadWords: words to designate sass
#sppechText: speech input from the user
def findKeyword(speechText, arrayOfBadWords, arrayOfKeywords):
    # print(speechText)
    forgottenItemArray = []
    foundItemArray = []
    badWordFound = False
    #Search for all the keywords using a loop
    for i in range(len(arrayOfKeywords)):
        index = speechText.find(arrayOfKeywords[i])
        #If a keyword was found pop the flag add it to the found items array, if not found find() returns -1
        if(index != -1):#if word is found, add it to the found item array
            foundItemArray.append(arrayOfKeywords[i])
        #If a keyword was not found, put it into the forgotten item array
        else: forgottenItemArray.append(arrayOfKeywords[i])
            
    #Search for all of the badwords using a loop
    for j in range(len(arrayOfBadWords)):
        badWordIndex = speechText.find(arrayOfBadWords[j])
    #if a badword was found mark pop the flag and return it at the end of tis function
        if badWordIndex != -1:
            badWordFound = True
    return forgottenItemArray, badWordFound