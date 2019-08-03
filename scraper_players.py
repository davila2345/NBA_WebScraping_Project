from string import ascii_lowercase
import os, time
import selenium
from selenium import webdriver
from pathlib import Path

# start browser crawler
browser = webdriver.Chrome(r'C:\Users\davil\Desktop\NYCDSA Bootcamp\bootcamp\July Course\chromedriver_win32\chromedriver.exe')

#function to scrape players bios on bballref
#players are grouped by first letter of last name and separated in each page
def scrapeBbalRefPlayers(page_string: object, id: object, folder_name: object) -> object:
	#note that no player in history of NBA has last name that starts with 'X'
	for letter in ascii_lowercase:
		#
		if letter == 'x':
			continue
		else:

			# navigate to bballref
			url = page_string.replace("*LETTER*", str(letter))
			browser.get(url)

			# setup id strings
			#partial_id = id + "_toggle_partial_table"
			csv_id = "csv_" + id

			# activate and grab data in CSV format
			#if toggle_partial:
			#	browser.execute_script('document.getElementById("'+ partial_id +'").click();')

			# grab raw CSV
			raw_csv = browser.execute_script('''var x = document.getElementsByClassName("tooltip");
			x[3].click();
			var content = document.getElementById("'''+ csv_id +'''")		
			return content.textContent
			''')
			print(raw_csv)		

			# write to CSV
			#print(f'"{raw_csv}"')
			#print(str("""+ raw_csv +"""))
			pathstr = Path(folder_name,f"{letter}_{id}.csv")

			f = open(pathstr, "w", encoding="utf-8")
			f.write(raw_csv)


scrapeBbalRefPlayers(page_string='https://www.basketball-reference.com/players/*LETTER*/',
	id='players',
	folder_name='players_bios'
)