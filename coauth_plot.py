# This programm aims to plot number of coauthors during 37 years of SEG annual meetings
# Filtered number of numb_articles
import matplotlib.pyplot as plt
import numpy as np
numb_articles = [302, 323, 407,	347,	292,	277,	388,	396,	517,	451,	383,	400,	466,	449,	585,	542,	549,	542,	636,	548,	627,	638,	663,	682,	714,	631,	741,	879,	873,	868,	899,	1017,	992,	1080,	1104,	1168,	1113]

ref_data = [2.285361,2.269854,2.285205,2.274893, 2.32184, 2.352931, 2.433209, 2.402235, 2.433422, 2.49702, 2.594231, 2.581554, 2.727233, 2.789873, 2.874077, 2.885946, 3.018021, 3.166208, 3.372227, 3.288681, 3.346355, 3.463061, 3.437281, 3.519684, 3.67232, 3.747994, 3.896395, 3.848252, 4.055962, 4.122729, 4.207524, 4.246959, 4.315808, 4.348695, 4.480921, 4.601956, 4.730707]


start_year = 1982
end_year = 2018
aver_coauth = []
filename = start_year
countcomma = 0
count = 0
year_num = 0

# file_out=open('coauthors_data.txt', 'w')

while filename < end_year+1:
    file=open(str(filename) + 'authors.txt', encoding="utf8")
    # file=open(name, encoding="utf8")
    count = 0
    coauth_array = []
    # name = ('1982authors.txt')
    # file=open(name, encoding="utf8")
    for line in file:
        countcomma = 0
        for chars in line:
            if chars == ',':
                countcomma = countcomma + 1
        coauth_array.append(countcomma + 1)
        count = count + 1
        # print(countcomma+1)
            # coauth_array[int(count)] = countcomma+1

    aver_coauth.append(sum(coauth_array)/len(coauth_array))
    # print(filename, sum(coauth_array), len(coauth_array)+1)
    # print('Year:', filename, file = file_out)
    # print(coauth_array, file = file_out)
    # print(count)
    filename = filename + 1
    file.close()
# print('Average coauthors for each year: ', file = file_out)
# print(aver_coauth, file = file_out)
# print('Number of articles for each year: ', file = file_out)
# print(numb_articles, file = file_out)
#
#
# file_out.close()
yr = 1982
for vals in aver_coauth:
    print(yr, vals)
    yr = yr + 1

t = aver_coauth
t.append(3.9009259259259259259259259259259)
print(t)
#
s = list(range(start_year, end_year+2, 1))
s1 = list(range(1980, 2017, 1))

# print(t)
# print(t[0])
# print(s[0])
# print(s[36])
# print(len(t), len(s))

plt.plot(s, t, 'b-', label="SEG Annual")
plt.plot(s1, ref_data, 'g-', label="Earth and planetary Science")


# plt.scatter(s, t, color='black')
plt.xlabel('Year')
plt.ylabel('Average co-authors')
plt.title('Increase of co-authors with time')
plt.grid(True)
plt.axis([1982, 2019, 1.9, 4.8])
# plt.yscale('log')
plt.legend()
plt.savefig("test.png")
plt.show()


# print(countcomma)
# countcomma = 0
