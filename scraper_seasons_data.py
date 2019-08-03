import os, time
import selenium
from selenium import webdriver
from pathlib import Path

#os.getcwd()
my_dir = 'C:/Users/davil/Desktop/test'

#my_dir = Path("C:","Users","davil","Desktop","test")

# start browser crawler
browser = webdriver.Chrome(r'C:\Users\davil\Desktop\NYCDSA Bootcamp\bootcamp\July Course\chromedriver_win32\chromedriver.exe')

def scrapeBbalRef(year_start: object, year_end: object, page_string: object, id: object, folder_name: object, toggle_partial: object = True) -> object:

	for season in range(year_start, year_end+1):
		#print(season)
		# navigate to bballref
		url = page_string.replace("*SEASON*", str(season))
		browser.get(url)

		# setup id strings
		partial_id = id + "_toggle_partial_table"
		csv_id = "csv_" + id

		# activate and grab data in CSV format
		if toggle_partial:
			browser.execute_script('document.getElementById("'+ partial_id +'").click();')

		# grab raw CSV
		raw_csv = browser.execute_script('''var x = document.getElementsByClassName("tooltip");
		x[3].click();
		var content = document.getElementById("'''+ csv_id +'''")
		// small hack to account for a few old MVP pages
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
		print(f'"{raw_csv}"')
		print(str("""+ raw_csv +"""))
		pathstr = Path(folder_name,f"{season}_{id}.csv")

		f = open(pathstr, "w", encoding="utf-8")
		f.write(raw_csv)


# scrape season player stat per game
scrapeBbalRef(year_start=1950, year_end=1959,
			  page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_per_game.html',
			  id='per_game_stats',
			  folder_name='season_stats_pergame'
			  )
# scrape season player stat totals
scrapeBbalRef(year_start=1950,year_end=1959,
			  page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_totals.html',
			  id='totals_stats',
			  folder_name='season_stats_totals'
			  )
# scrape season advanced player stats
scrapeBbalRef(year_start=1950,year_end=1959,
			  page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_advanced.html',
			  id='advanced_stats',
			  folder_name='season_stats_advanced'
			  )
# # scrape MVP stats
scrapeBbalRef(year_start=1956,year_end=1959,
			  page_string='https://www.basketball-reference.com/awards/awards_*SEASON*.html',
			  id='nba_mvp',
			  folder_name='award_stats',
			  toggle_partial=False
			  )
# # scrape standings stats
scrapeBbalRef(year_start=1950,year_end=1959,
			  page_string='https://www.basketball-reference.com/leagues/NBA_*SEASON*_standings.html',
			  id='expanded_standings',
			  folder_name='season_standings',
			  toggle_partial=False
			  )
