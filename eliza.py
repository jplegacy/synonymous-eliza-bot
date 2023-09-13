
import random
import sys

class JeremyChatAgent: 
    """
    Basic Eliza-Based Chatbot which can be set up as a Slackbot.

    Follow instructions as defined on https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/
    """
   
    def generateReply(self,inString):
       """Pick a random function, and call it on the input string """
       randFunction = random.choice(self.ReplyFunctionList)
       reply = randFunction(inString) 
       return reply + ":"
 
    def driverLoop(self):
       """The main driver loop for the chat agent"""
       reply = "how are you today?"
       self.historyResponse.append(reply)

       
       while True:
           response = input(reply)
           self.historyInput.append(response)

           reply = self.generateReply(response)
           self.historyResponse.append(reply)

           self.recordDialog(response,reply)

    
    def reply(self, dialog):
        response = dialog
        self.historyInput.append(response)

        reply = self.generateReply(response)
        self.historyResponse.append(reply)

        self.recordDialog(response,reply)

        return reply

    def recordDialog(self, inputs, output):
        self.historyInput.append(inputs)
        self.historyResponse.append(output)
        
        if not self.longConversation  and len(self.historyResponse) == self.MAXHISTORYMEMORY:
            self.longConversation = True
            self.ReplyFunctionList.append(self.reflectiveFeedback)
            self.ReplyFunctionList.append(self.elaborateDifferently)
            
        if len(self.historyResponse) == self.MAXHISTORYMEMORY:
            self.historyInput.pop(0)
            self.historyResponse.pop(0)
            
    def swapPersonTerm(self,inWord):
       """Replace 'I' with 'You', etc"""
       if (inWord in self.PronounDictionary.keys()):   #if the word is in the list of keys
           return self.PronounDictionary[inWord] 
       else:
           return inWord

    
    def switchPerson(self,inString):
       """change the pronouns etc of inString
       by iterating through the PrononDictionary
       and substituting keywords for subwords
       """
       
       inWordList = str.split(inString)
       switched = map(self.swapPersonTerm, inWordList)

       reply = ' '.join(switched)  #glue things back together
       return reply 

    def changePersonAndAddPrefix(self,inString):
        reply = self.switchPerson(inString)
        randomPrefix = random.choice(self.PrefixList)
        return ''.join([randomPrefix,reply])

  
    def generateHedge(self,inString):
        return random.choice(self.HedgeList);

    def reflectiveFeedback(self,inString):
        selfReflectQuestion = random.choice(self.selfReflectQuestionList)
        randomResponse = random.choice(self.historyResponse)

        return ''.join([selfReflectQuestion, randomResponse])
   
    def elaborateDifferently(self,inString):
        explainQuestion = random.choice(self.explainPreviousList)
        randomInput = random.choice(self.historyInput[:self.MAXHISTORYMEMORY-2]) #wont include the last response
        question = random.choice(self.questions) 

        return ''.join([explainQuestion, randomInput,question])
    
    
    def interstingTerm(self, inString):
        inWordList = str.split(inString)
        longest = max(inWordList, key=len)
        
        return longest
    
    def termWonder(self,inString):
        term = self.interstingTerm(inString)
        explainatoryQue = random.choice(self.questionList)
        corr = random.choice(self.correlationList)


        return ''.join([explainatoryQue, term,corr])


            
    def __init__(self):
       
       self.MAXHISTORYMEMORY = 10 #the number of responses that the bot will remember 

       self.PronounDictionary = {'i':'you','I':'you','am':'are', 'you':'I', 'me':'you'}
       self.HedgeList = ["Hmm","That is fascinating","Let's change the subject", "Perhaps", "To some extent", "Sometimes"]
       self.PrefixList = ["Why do you say that ","What do you mean that ", "Well why wouldn't you say ", "Are you sure that ", "Could you explain what you meant by ", "What do you think of "]
              
       self.selfReflectQuestionList = ["how did it affect you earlier when I said ", "how did you feel after I said "]
       self.historyResponse = []

       self.explainPreviousList = ["you previously said "]
       self.historyInput = []
       self.questions = [", how does this change things", ", how does this affect your life"]

       self.questionList = ["What does ", "What will "]
       self.correlationList = [" mean to you", " mean to this world"]

       self.ReplyFunctionList = [self.generateHedge,self.changePersonAndAddPrefix, self.termWonder] #this is what makes Python so powerful
   
       self.longConversation = False

   #End of ChatAgent

if __name__ == '__main__': #will only be called if this is invoked directly by python, as opposed to included in a larger file
    
    #version checking
    MIN_PYTHON = (3, 7)
    assert sys.version_info >= MIN_PYTHON, "requires Python 3, run with `python3 eliza.py`"

    #program starts here
    random.seed() #if given no value, it uses system time
    agent = JeremyChatAgent()
    agent.driverLoop()
