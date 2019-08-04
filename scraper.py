import os, time
import selenium
from selenium import webdriver
from pathlib import Path
from string import ascii_lowercase


# start browser crawler --> Windows users: make sure you know where chromedriver.exe file is
browser = webdriver.Chrome(r'C:\chromedriver.exe')

################## function to scrape players bios on bballref ##########################
#must loop through alphabet as players are grouped and separated by first letter of last name
def scrapeBbalRefPlayers(page_string: object, id: object, folder_name: object) -> object:
	for letter in ascii_lowercase:
		#note that no player in history of NBA has last name that starts with 'X'
		if letter == 'x':
			continue
		else:
			# navigate to bballref
			url = page_string.replace("*LETTER*", str(letter))
			browser.get(url)

			# setup id strings
			csv_id = "csv_" + id

			# extract values raw_CSV
			raw_csv = browser.execute_script('''var x = document.getElementsByClassName("tooltip");
			x[3].click();
			var content = document.getElementById("'''+ csv_id +'''")		
			return content.textContent
			''')
			#print(raw_csv)		

			# write to CSV in desired folder
			pathstr = Path(folder_name,f"{letter}_{id}.csv")
			f = open(pathstr, "w", encoding="utf-8")
			f.write(raw_csv)


scrapeBbalRefPlayers(page_string='https://www.basketball-reference.com/players/*LETTER*/',
	id='players',
	folder_name='players_bios'
)

################ function to scrape NBA and ABA champions ################################
# no need to loop through seasons --> all seasons are included on one page
def scrapeBbalRefChamps(page_string: object, id: object, folder_name: object) -> object:
	# navigate to bballref
	browser.get(page_string)

	# id string for grabbing csv values
	csv_id = "csv_" + id

	# grab raw CSV
	raw_csv = browser.execute_script('''var x = document.getElementsByClassName("tooltip");
		x[3].click();
		var content = document.getElementById("'''+ csv_id +'''")		
		return content.textContent
		''')
	#deleting extra row abover header columns
	raw_csv = '\n'.join(raw_csv.split('\n')[2:])
	print(raw_csv)		

	# write to CSV
	pathstr = Path(folder_name,f"{id}.csv")

	f = open(pathstr, "w", encoding="utf-8")
	f.write(raw_csv)

	browser.close()

scrapeBbalRefChamps(page_string = "https://www.basketball-reference.com/playoffs/",
	id = 'champions_index',
	folder_name = 'champs')

########### Function to loop through links designated by season and scrape relevant stats ###############
def scrapeBbalRef(year_start: object, year_end: object, page_string: object, id: object, folder_name: object, toggle_partial: object = True) -> object:

	for season in range(year_start, year_end+1):
		# navigate to bballref
		url = page_string.replace("*SEASON*", str(season))
		browser.get(url)

		# setup id strings
		partial_id = id + "_toggle_partial_table"
		csv_id = "csv_" + id

		# toggle to show all teams a player who changed teams during season played for
		if toggle_partial:
			browser.execute_script('document.getElementById("'+ partial_id +'").click();')

		# extract values for raw_CSV
		raw_csv = browser.execute_script('''var x = document.getElementsByClassName("tooltip");
			x[3].click();
			var content = document.getElementById("'''+ csv_id +'''")
			// different element id in some older MVP pages
			if (content==null) {
				var content = document.getElementById("csv_mvp")
				}
			return content.textContent
			''')
		raw_csv		

		# clean csv string
		## get rid of false headers
		if page_string == 'https://www.basketball-reference.com/awards/awards_*SEASON*.html' or \
						page_string == 'https://www.basketball-reference.com/leagues/NBA_*SEASON*_standings.html':
			raw_csv = '\n'.join(raw_csv.split('\n')[2:])
		## remove special characters from standings
		raw_csv=raw_csv.replace("\u2264","")
		raw_csv=raw_csv.replace("\u2265","")


		# write to CSV
		pathstr = Path(folder_name,f"{season}_{id}.csv")
		f = open(pathstr, "w", encoding="utf-8")
		f.write(raw_csv)

### Using function to....
# scrape season player stat per game
scrapeBbalRef(year_start=1950, year_end=2019,
	page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_per_game.html',
	id='per_game_stats',
	folder_name='season_stats_pergame'
	)
# scrape season player stat totals
scrapeBbalRef(year_start=1950,year_end=2019,
	page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_totals.html',
	id='totals_stats',
	folder_name='season_stats_totals'
	)
# scrape season advanced player stats
scrapeBbalRef(year_start=1950,year_end=2019,
	page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_advanced.html',
	id='advanced_stats',
	folder_name='season_stats_advanced'
	)
# scrape MVP stats
scrapeBbalRef(year_start=1956,year_end=2019,
	page_string='https://www.basketball-reference.com/awards/awards_*SEASON*.html',
	id='nba_mvp',
	folder_name='award_stats',
	toggle_partial=False
	)
# scrape standings stats
scrapeBbalRef(year_start=1950,year_end=2019,
	page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_standings.html',
	id='expanded_standings',
	folder_name='season_standings',
	toggle_partial=False
	)
# scrape playoffs player stats per game
scrapeBbalRef(year_start=1950, year_end=2019,
	page_string='https://www.basketball-reference.com/playoffs/NBA_*SEASON*_per_game.html',
	id='per_game_stats',
	folder_name='playoffs_stats_pergame',
	toggle_partial=False
	)
#scrape playoffs player stats totals
scrapeBbalRef(year_start=1950,year_end=2019,
	page_string='https://www.basketball-reference.com/playoffs/NBA_*SEASON*_totals.html',
	id='totals_stats',
	folder_name='playoffs_stats_totals',
	toggle_partial=False
	)
#scrape playoffs advanced player stats
scrapeBbalRef(year_start=1950,year_end=2019,
	page_string='https://www.basketball-reference.com/playoffs/NBA_*SEASON*_advanced.html',
	id='advanced_stats',
	folder_name='playoffs_stats_advanced',
	toggle_partial=False
	)
