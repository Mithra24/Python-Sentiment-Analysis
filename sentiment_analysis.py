import re
# library imported to perform stemming of the words
from nltk.stem import LancasterStemmer

# dictionary created to store bag of words based on ratings 
bag={1:[],2:[],3:[],4:[],5:[]}
#list created to store positive and negative words
positive_words=[]
negative_words=[]

# initializes the object for stemming
lancaster=LancasterStemmer()

# method created to remove stop words
def word_extraction(sentence):    
    ignore = ['a', "the", "is"]    
    words = re.sub("[^\w]", " ",  sentence).split()    
    cleaned_text = [lancaster.stem(w.lower()) for w in words if w not in ignore]    
    return cleaned_text
    
# create tokens and return distinct words    
def tokenize(sentence):    
    words = []    
    w = word_extraction(sentence)        
    words.extend(w)          
        
    words = sorted(list(set(words)))    
    return words
    
# create vector having frequency of the words
def generate_bow(vocab):            
    bag_vector={}
    for w in vocab:            
        if w in bag_vector:
            bag_vector[w] += 1 
        else:
            bag_vector[w] = 1
    return bag_vector

# reads all the reviews and create rating wise bags
def load_dataset():
    i=1
	#open file
    f = open("Diablo-III-PC reviews.txt", "r")

    for x in f:
		# read only rating value
        if i%7==1:
            rating=int(float(x.split(" ")[1]))

		#read only review and store in corresponding bag
        if i%7==0:
            review=x.split(":")[1] 
            bag[rating].extend(tokenize(review))
        i=i+1

# read words for testing 
# stemming is done for the words
def load_words():
    f = open("positive-words.txt", "r")
    for x in f:
        positive_words.append(lancaster.stem(x.strip().lower()))

    f = open("negative-words.txt", "r")
    for x in f:
        negative_words.append(lancaster.stem(x.strip().lower()))
 
# method to calulate sentiment polarity by multiplying the 
# frequency with ratings 
def calculate_sentiments(word):
    numerator=0
    denominator=0
    
    for i in bag:
        result=generate_bow(bag[i])
        
        if word in result:
            numerator=numerator+result[word]*i
            denominator=denominator+result[word]

    sentiment=0
    if denominator>0:
        sentiment=round(float(numerator)/float(denominator),1)
    return sentiment
        

#calling of the methods
load_dataset()
load_words()

most_positive={}
most_negative={}

# calculating sentiment polarity for all words
# and sorting decending based on value
# and extracting top 10 from positive
# and negative.
for i in list(set(positive_words)):
    word= i.strip()
    sentiment=calculate_sentiments(word)
    if word not in most_positive:
        most_positive[word]=sentiment
 
for i in list(set(negative_words)):
    word= i.strip()
    sentiment=calculate_sentiments(word)
    if word not in most_negative:
        most_negative[word]=sentiment

print ("10 Most Positive words:")        
print (sorted([(key) for (key,value) in most_positive.items()],reverse=True) [:10])

print ("10 Most Negative words:")   
print (sorted([(key) for (key,value) in most_negative.items()],reverse=True) [:10])