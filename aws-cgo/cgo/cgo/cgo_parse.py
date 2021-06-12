#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cgo_parse1.py - program to automate the parsing of data from the site of the CGO
# and store the received data in a .csv file

import os
import bs4
import csv
import requests
from datetime import datetime
#Connect to the site
try:
    res = requests.get('http://cgo-sreznevskyi.kyiv.ua/index.php?fn=lsza&f=lsza')
    res.raise_for_status()
except requests.exceptions.HTTPError as err:
    print('Connection error.')

#Extract tables
print(res.text)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
tableElems = soup.findAll('table', attrs={'cellspacing' : '0', 'border' : '1'})

#We create the list where we will add all elements of columns and lines
cogData = []
#general list of column names
columnsList = []
#Create a row where we add the name of the columns of the table 7
columns_1 = []
thElems = tableElems[0].findAll('th')
for th in thElems:
    header = th.string
    columns_1.append(header)
del columns_1[2]
#save a row of columns for each table separately
columnsList.append(columns_1)
#Create a row where we add the name of the columns of the table 20
columns_2 = []
thElems = tableElems[1].findAll('th')
for th in thElems:

    header = th.string

    columns_2.append(header)

del columns_2[2]

columnsList.append(columns_2)



#Create a row where we add the name of the columns of the table 3

columns_3 = []

trElem = tableElems[2].find('tr')

b = trElem.findAll('b')

for elem in b:

    header = elem.string



    #change \xa0 for spaces

    header = header.replace(u'\xa0', u' ').strip()

    columns_3.append(header)

columnsList.append(columns_3)



#Create a row, where we add the name of the columns of table number 0

columns_4 = []

trElem = tableElems[4].find('tr')

tdElem = trElem.findAll('td')

for elem in tdElem:

    pElem = elem.findAll('p')

    header = ''

    for p in pElem:

        p = str(p.string)

        if p == 'None':

            header += ''

        else:

            header += p + ' '

    header = header.strip()

    columns_4.append(header)

columnsList.append(columns_4)



#counter for proper mapping of tables to columns

i = 0



#find the values ​​of tables 7 and 20 and write them into the table

tableElems_1 = tableElems[:2]

for table in tableElems_1:

    tableData = []

    tableData.append(columnsList[i])

    trElems = table.findAll('tr')

    for tr in trElems:

        tdElems = tr.findAll('td')



        #we exclude empty lines in the table (CSS lines)

        if (tdElems != None) and (len(tdElems) != 1):

            rowList = []

            for td in tdElems:

                value = td.string



                #remove extra spaces

                value = value.replace(u'\xa0', u' ').strip()

                rowList.append(value)



            #add values ​​to the list

            tableData.append(rowList)

    cogData.append(tableData)

    i += 1



#find the values ​​of tables 3 and 5 and write them in the table

for table in tableElems[2:4]:

    tableData = []

    tableData.append(columnsList[2])

    trElems = table.findAll('tr')

    for tr in trElems[1:]:

        tdElems = tr.findAll('td')

        rowList = []

        for td in tdElems:

            value = td.string



            #Find empty lines

            if value == None:

                value = ''



            else:

                value = value.strip()

            rowList.append(value)

        tableData.append(rowList)

    cogData.append(tableData)



#find the values ​​of table number 0 and write them to the table

trElems = tableElems[4].findAll('tr')

tableData = []

tableData.append(columnsList[3])

for tr in trElems[1:]:

    tdElems = tr.findAll('td')

    rowList = []

    for td in tdElems:

        pElems = td.findAll('p')

        header = ''

        for p in pElems:

            p = str(p.string)

            if p == 'None':

                header += ''

            else:

                header += p + ' '

        header = header.strip()

        rowList.append(header)

    tableData.append(rowList)

cogData.append(tableData)



#Save data

#create a new folder

os.makedirs('data', exist_ok=True)

os.chdir('data')



#List for numbering points (tables) and matching numbering with files

number_table = ['7', '20', '3', '5', '0']



#Write the table data to a file

for t in range(len(cogData)):



	#add point number and name

	date_now = datetime.strftime(datetime.now(), "%Y-%m-%d")

	filename = 'cgo_' + number_table[t] + '_' + date_now + '.csv'



	#set the encoding to display correctly and write the file

	with open(filename, 'w', encoding='utf-8') as file:

		writer = csv.writer(file)

		writer.writerows(cogData[t])
