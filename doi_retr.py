from crossref.restful import Works
import ast

input_doi = open('C:\\Users\\Tima\\Desktop\\python\\doi_ref.txt', 'r', encoding="utf8")
output_doi = open('C:\\Users\\Tima\\Desktop\\python\\2019org_out.txt', 'w', encoding="utf8")
data = input_doi.read()
splitted = data.split('\n')
works = Works()
counter = 0
count = 0
coauthors = []


for line in splitted:
    output = works.doi(line)
    ttt = output['author']
    # print(len(ttt))
    dict = {}
    dict_af = {}
    if len(ttt) > 1:
        for count in range(0, len(ttt)):
            # print(count, ttt[count])
            dict = ast.literal_eval(str(ttt[count]))
            fff = dict['affiliation']

            dict_af = ast.literal_eval(str(fff[0]))
            print(dict_af['name'], file = output_doi)

    else:
        dict = ast.literal_eval(str(ttt[0]))
        fff = dict['affiliation']
        dict_af = ast.literal_eval(str(fff[0]))
        print(dict_af['name'], file = output_doi)


    # coauthors.append(len(output['author']))
    # counter +=1
    # if counter == 15:
    #     quit()

# print(coauthors)
# print(sum(coauthors)/len(coauthors))
# print('Счётчик: ', counter, 'Длина: ', len(coauthors))
