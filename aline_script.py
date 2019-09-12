import re

word = 'Melbourne'

file_inp = open('C:\\temp\\txtan\\organization\\organization\\not_in_list.txt', 'r', encoding="utf8")
file_out = open('C:\\temp\\txtan\\organization\\organization\\not_in_list_write.txt', 'w', encoding="utf8")
data = file_inp.read()
my_list = data.split("\n")
# xline = re.findall(r'something', line)[0]
my_list2= my_list

out_list = []

for word in my_list2:
    # print('\''+item+'\'', file = file_out)
    for element in my_list:
        if word.casefold() in element.casefold():
        # if word in element:
            out_list.append(element)
    # "Petro-Canada" : ('PetroCanada','Petro-Canada', 'Petro-Canada Netherlands BV'),
    if len(out_list) > 1:
        # print(len(out_list), out_list)
        print('\"'+out_list[0]+'\"', end = ' : (', file = file_out)
        for ii in range(0, len(out_list)-1):
                print('\''+out_list[ii]+'\'', end = ', ' , file = file_out)

        print('\''+out_list[len(out_list)-1]+'\'', end = '' , file = file_out)
        print('', end = '), ' , file = file_out)
        print('', file = file_out)


        #     print('', file = file_out)
        #
    # print('\"'+out_list[0]+'\"', end = ' : (', file = file_out)
    # for ii in range(0, len(out_list)):
    #
    #     if ii == len(out_list)-1:
    #         print('\''+out_list[ii]+'\'', end = '' , file = file_out)
    #     else:
    #         print('\''+out_list[ii]+'\'', end = ', ' , file = file_out)
    #
    # print('', end = '), ' , file = file_out)
    # print('', file = file_out)


    out_list = []
quit()

for element in my_list:
    # if word.casefold() in element.casefold():
    if word in element:
        out_list.append(element)

print('\"'+out_list[0]+'\"', end = ' : (')
for ii in range(0, len(out_list)):

    if ii == len(out_list)-1:
        print('\''+out_list[ii]+'\'', end = '' )
    else:
        print('\''+out_list[ii]+'\'', end = ', ' )

print('', end = '), ' )
