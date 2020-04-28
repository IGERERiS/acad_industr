# for making sqllite database from all si, bi, tri, - gramms
import sqlite3
import json
import ssl
import sys
import matplotlib.pyplot as plt
import numpy as np
import operator
# Output dictionary
dict = {}
# Yearly dictionary
dict_yearly = {}
# All words dictionary
all_words = {}
# start_year - first year of data, end_year - last year of data
start_year = 1982
end_year = 2019

conn = sqlite3.connect('grams.sqlite')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS WordsData (words TEXT, '1982-2019' TEXT)''')
# if int(word_type) == 1: an_type = '_sigrams.tsv'
# if int(word_type) == 2: an_type = '_bigrams.tsv'
# if int(word_type) == 3: an_type = '_trigrams.tsv'

# word_type = ['_sigrams', '_bigrams', '_trigrams']
an_type = '_trigrams.tsv'
filename = start_year
# numb_pages - Number of pages for corresponding year 1982 - 2018, 37 years in total
# numb_articles -Number of articles for corresponding year 1982 - 2018, 37 years in total
numb_pages = [520,	646,	856,	643,	715,	923,	1359,	1375,	1779,	1646,	1410,	1396,	1679,	1566,	2106,	2067,	2092,	2061,	2484,	2135,	2478,	2452,	2586,	2668,	3541,	3124,	3713,	4338,	4453,	4424,	4609,	5258,	5183,	5634,	5654,	6093,	5520, 5407]
# After filtering pp. number (which are workshop marks)
numb_articles = [302,	323,	407,	347,	292,	277,	388,	396,	517,	451,	383,	400,	466,	449,	585,	542,	549,	542,	636,	548,	627,	638,	663,	682,	714,	631,	741,	879,	873,	868,	899,	1017,	992,	1080,	1104,	1168,	1113, 1080]
aver_weight = [1.756434027,	2.24470738,	3.129408928,	2.24875279,	2.19130921,	1.959459517,	2.857542142,	2.825285165,	3.113519538,	3.108913421,	2.450975564,	3.074120705,	3.918190738,	3.616456154,	4.508389261,	4.483344754,	4.426535868,	4.171001424,	4.977122668,	4.203568171,	4.681508658,	4.861086588,	5.321508315,	5.738341425,	6.173885861,	5.79084917,	6.912996051,	8.142251078,	8.277925853,	7.774938297,	8.41737085,	9.242705308,	9.213967767,	9.964783212,	10.25742826,	10.79747233,	10.17245022]

# Filename change
while filename < end_year+1:
# collects all words in a list
# making big dictionary
    file=open(str(filename) + an_type)
    filename = filename + 1
    for line in file:
      line = line.replace('\n', '')
      key, value = line.split("\t")
      all_words.setdefault(key, [])

    file.close()

filename = start_year

while filename < end_year+1:
# open files with grams and make dictionaries
# collecting values for words
    file=open(str(filename) + an_type)

    for line in file:
      line = line.replace('\n', '')
      key, value = line.split("\t")
      dict_yearly.setdefault(key, [])
      all_words[key].append(int(value))

# if word doesn't appear this year, 0 will be added
    for key, value in all_words.items():
        if key not in dict_yearly:
            all_words[key].append(int(0))

    dict_yearly = {}

    filename = filename + 1
    file.close()

dict_sum = {key: sum(values) for key, values in all_words.items()}
count = 0

no_sorted_dict = {}
count = 0

for key, value in all_words.items():
    if sum(value) > 15:
        cur.execute('''INSERT INTO WordsData (words, '1982-2019')
                VALUES ( ?, ? )''', (key, str(value)) )
        conn.commit()
        count = count + 1
        if (count/1000).is_integer():
            print('1000 proletelo')
    else:
        continue
quit()
# sorted_dict = sorted(no_sorted_dict.items(), key=operator.itemgetter(1))

for key, value in sorted_dict:
    print(key, value, file = file_out)

# Asking the operator which words to check
input_word= input('Which word do you want to check?')
if len(input_word) < 1 :
    if int(word_type) == 1: input_word = 'electromagnetic'
    if int(word_type) == 2: input_word = 'seismic wave'
    if int(word_type) == 3: input_word = 'full waveform inversion'

t = all_words_norm[input_word][:]
if int(word_type) == 2:
    word_reverse = input_word.split(' ')
    word_reverse = str(word_reverse[1]+' '+word_reverse[0])

    try:
        t_add = all_words_norm[word_reverse][:]
        t= [i + j for i, j in zip(t, t_add)]
    except:
        pass

s = list(range(start_year, end_year+1, 1))

# Setting scale for the graphs
maximum = max(t[8:])+max(t[8:])*0.1
minimum = round(min(t[8:])-1)
if minimum < 0:
    minimum=0

plt.plot(s, t)
# plt.scatter(s, t, color='black')
plt.xlabel('Year')
plt.ylabel('Occurence/pages')
plt.title('Occurence of ' +'"' + input_word +'"')
plt.grid(True)
# plt.axis([1990, 2019, minimum, maximum])
plt.axis([1982, 2019, minimum, maximum])

plt.savefig("test.png")
plt.show()
