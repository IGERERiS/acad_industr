# Function to make word cloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud


start_year = 1982
end_year = 2018
name = start_year

while name < end_year+1:

    handle = open(str(name) + '_bigrams.tsv', 'r')

    d = {}
    for line in handle:
        words = line.split('\t')
        # words[1].rstrip('\n')
        d[words[0]] = int(words[1])


    wordcloud = WordCloud(width=1000, height=600)
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig(str(name)+'.png')

    #clear plot
    plt.clf()
    plt.close('all')
    name = name + 1
