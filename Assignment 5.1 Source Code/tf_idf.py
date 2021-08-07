import re
import math
import numpy as np
import matplotlib.pyplot as plt

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
import itertools

urls = [
        "https://www.aorus.com/en-ph/graphics-cards/GV-N3090AORUSX-W-24GD/Key-Features",
        "https://www.aorus.com/en-ph/graphics-cards/GV-N308TAORUSX-W-12GD",
        "https://www.aorus.com/en-ph/graphics-cards/GV-N3080AORUSX-W-10GD-rev-20",
        "https://www.aorus.com/en-ph/graphics-cards/GV-N3080AORUSX-WB-10GD-rev-10",
        "https://www.aorus.com/en-ph/monitors/AORUS-FO48U",
        "https://www.carwow.co.uk/new-car-deals",
        "https://www.porsche.com/pap/_philippines_/models/718/718-models/718-cayman/",
        "https://www.porsche.com/pap/_philippines_/models/911/911-models/",
        "https://www.porsche.com/pap/_philippines_/models/taycan/taycan-models/",
        "https://www.porsche.com/pap/_philippines_/models/macan/macan-models/",
]

def all_words_list(urls):

    all_words = []

    for url in urls:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()  
        text = soup.get_text()
        text = re.sub(r'[^\w]', ' ', text)
        bagofwords = text.split(' ')
        bagofwords = [x for x in bagofwords if x]
        all_words.append(bagofwords)

    return all_words

def list_struct(): return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

all_words = all_words_list(urls)
words_tf = defaultdict(list_struct)
words_idf = {}
words_tf_idf = defaultdict(list_struct)
words_tf_idf_sum = {}

for i in range(len(all_words)):
    words = all_words[i]
    n = len(words)
    for word in words:
        tf_list = words_tf[word]
        tf_list[i] = ((tf_list[i] * n) + 1) / n
        words_tf[word] = tf_list

for key in words_tf.keys():
    zero = words_tf[key].count(0)
    f = 10 - zero

    words_idf[key] = math.log10(10/f)


for key in words_tf.keys():
    Sum = 0.0
    for i in range(len(words_tf[key])):
        tf = words_tf[key][i]
        score = tf * words_idf[key]
        Sum += score
        words_tf_idf[key][i] = score
    words_tf_idf_sum[key] = Sum

words_tf_idf_sum = dict(sorted(words_tf_idf_sum.items(), key=lambda item: item[1], reverse=True))

sliced_words_tf_idf_sum = dict(itertools.islice(words_tf_idf_sum.items(), 30))
x = list(sliced_words_tf_idf_sum.keys())
y = list(sliced_words_tf_idf_sum.values())

ind = np.arange(len(y))

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)
#fig.savefig('test2png.png', dpi=100)
ax.barh(ind, y)
ax.set_yticks(ind)
ax.set_yticklabels(x)

ax.bar_label(ax.containers[0])
plt.gca().invert_yaxis()
plt.title("THE TOP 30 MOST RELEVANT WORD IN 10 WEBSITES")
plt.show()