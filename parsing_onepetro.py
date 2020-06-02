# coding=utf8
# Aim of this program is to create and use database of common authorship
# We want to know who are collaborators of different service companies
# Timofey Eltsov
# May 29, 2020
import re
import sqlite3

start_year = 1980
end_year = 2020
name = start_year
count = 0
year_num = 0
total_list = []
industry_list = []
first_step = []
industry_dict = {}
soc_ind = ''
paper_title = ''
org_count_total = 0


conn = sqlite3.connect('onepetro_metadata.sqlite')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS Metadata (Year TEXT, Society TEXT, Publicationtype Text,  Title TEXT, Affiliations TEXT, Authors TEXT)''')

while name < end_year+1:
# Counter of organization
    # print('Processing year...#', name)
    block_of_lines = []
    file=open(str(name) + '.txt', encoding="utf8")
    data = file.read()
    data = data.replace('View rights & permissions\n','')
    data = data.replace('Get PDF Export citation\n', '')
    data = data.replace('Add to cart Export citation\n', '')
    data = data.replace(' Administration log out', '')
    first_step = data.split('\nExport citations\n')
    separate_pap = first_step[1].split('Quick AbstractMetrics\n')

    # print(len(separate_pap))
    # print(separate_pap[100])
    for elemelo in separate_pap:
        count +=1
        list_one_paper = []
        author = ''
        authorS = []
        listing = elemelo.split('\n')
        soc_ind     = listing[0]
        paper_title = listing[1]
        paper_type = listing[len(listing)-2]
        # print(soc_ind)
        # print(paper_title)
        # print(paper_type)

        for element in listing[2:len(listing)-2]:
            temp_line = element.split(', ')
            companiero = element[len(temp_line[0])+len(temp_line[1])+4:]
            companiero = companiero.replace(',', '')
            author = temp_line[:2]
            list_one_paper.append(companiero)
            authorS.append(author)
        
        cur.execute('''INSERT INTO Metadata (Year, Society, Publicationtype, Title, Affiliations, Authors)
                    VALUES ( ?, ?, ?, ?, ?, ? )''', (name, str(soc_ind), str(paper_type), str(paper_title), str(list_one_paper), str(authorS) )) 
        conn.commit()

    
    quit()
        
    print(len(separate_pap))
    
    # #  'Journal Paper'
    # # 'Conference'

    
    # temp_line = []
    # listing = []    
    # temp_str = ''
    # soc_ind = 'SPE'
    # for match in raw_data:
    #     count +=1
    #     list_one_paper = []
    #     author = ''
    #     authorS = []
    #     listing = match.split('\n')
    #     paper_title = listing[0]
    #     # listing = listing[2:len(listing)-1]
        
    #     for element in listing[1:len(listing)-4]:
    #         temp_line = element.split(', ')
    #         companiero = element[len(temp_line[0])+len(temp_line[1])+4:]
    #         companiero = companiero.replace(',', '')
    #         author = temp_line[:2]
    #         list_one_paper.append(companiero)
    #         authorS.append(author)
        
      
    

        
    #     if (count/1000).is_integer():
    #         print(count, '1000 proletelo')
    # print(count)
    # quit()
    name += 1   
    
    file.close()
