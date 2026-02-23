import sys
import requests
from bs4 import BeautifulSoup

#input check
if len(sys.argv) < 3:
    print("provide 2 correct urls")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

#get words,their counts
def get_words(url):
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    text = s.body.get_text().lower()
    dict_counts = {}
    for w in text.split():
        if len(w) > 3: 
            if w in dict_counts:
                dict_counts[w] += 1
            else:
                dict_counts[w] = 1
    return dict_counts

#hashing
def hashfunc(word):
    h = 0
    for char in word:
        h = (h * 31 + ord(char)) % (2**64)
    return h

#simhash
def get_simhash(counts):
    v = [0] * 64
    for word in counts:
        w_hash = hashfunc(word)
        weight = counts[word]
        for i in range(64):
            if (w_hash >> i) & 1:
                v[i] += weight
            else:
                v[i] -= weight
    
    final = 0
    for i in range(64):
        if v[i] > 0:
            final |= (1 << i)
    return final

#comparing
data1 = get_words(url1)
data2 = get_words(url2)

hash1 = get_simhash(data1)
hash2 = get_simhash(data2)

match = 0
for i in range(64):
    bit1 = (hash1 >> i) & 1
    bit2 = (hash2 >> i) & 1
    if bit1 == bit2:
        match += 1

print("Similarity", match)