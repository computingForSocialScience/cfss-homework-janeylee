import nltk
import requests
#SENSE AND SENSIBILITY by Jane Austen (1811)
url = 'http://www.gutenberg.org/files/161/161.txt'
req = requests.get(url)
raw = req.text
start = raw.find("CHAPTER 1")
end = raw.rfind("End of the Project Gutenberg")
raw = raw[start:end]

tokens = nltk.word_tokenize(raw)
print "Number of tokens is %d" % len(tokens)

text = nltk.Text(tokens)
fdist = nltk.FreqDist(text)
print fdist['the']

bigrams = list(nltk.bigrams(text))
trigrams = list(nltk.trigrams(text))
print list(trigrams)[0:20]

pos = nltk.pos_tag(tokens[0:13]) #tells you what kind of words they are
print pos

stopwords = nltk.corpus.stopwords.words('english')
text2 = [w for w in text if w.lower() not in stopwords]
