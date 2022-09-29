""""
from requests_html import HTMLSession

s = HTMLSession()

query = 'Manchester City'
url = 'https://projects.fivethirtyeight.com/soccer-predictions/premier-league/'

r = s.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0'})

print(r.html.find('data-str=Manchester.City', first = True))
"""

# This is a method of scraping table data from online (generally tagged in html as <table>)
# Install packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import csv
import os

# Site URL
url="https://projects.fivethirtyeight.com/soccer-predictions/premier-league/"

# GET request to fetch the raw html content
html_content = requests.get(url).text

# Parse HTML code for the entire site
soup = BeautifulSoup(html_content, 'lxml')
#print(soup.prettify())

# Just checking how many tables there are on the page so we only get the one
premleague = soup.find_all("table")
print("Number of tables on site: ", len(premleague))

# For reproducibility, lets pretend there are more than one tables and we want just the first (the 0th index in Python speech)
# Scrape the first table
table1 = premleague[0]
# Head will form our column names 
body = table1.find_all("tr")
# Head values are teh first itesm of the body list
head = body[2] # ie the 0th item is the header row #note we can change this to 2 to get the right headings
bodyrows = body[3:] # every other item apart from the 0th make up the rest of the rows in the table # note we've changed this to 3rd item and beyond because 2nd item is the column

# Unsure if this will work but lets see
# Iterate through the head html code and make list of clean headings
headings = []
for item in head.find_all("th"): # loop through all the th elements
    # conver the the elements to text and strip \n
    item = (item.text).rstrip("\n")
    # append clean column name to headings
    headings.append(item)
print(headings)
# Issue is the table has two sets of headers - we need the second row.
# If we change head to body[2], we get the right values...

# Now to loop through the rest of the rows
all_rows = [] # this is going to be a list for list of all rows
for row_num in range(len(bodyrows)): # A row at a time
    row = [] # to hold old entires for one row
    for row_item in bodyrows[row_num].find_all("td"): # loop through all row entries
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma seperates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        # append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)

# So now we can use the data on all_rowsa and heading to make a table
# all_rows becomes our data and headings the column names
df = pd.DataFrame(data=all_rows,columns=headings)
df.head()
print(df)
df

df.to_csv('\out.csv')