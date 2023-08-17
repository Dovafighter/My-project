import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#################
# Get names of games that are currently available in PS Extra and make a list out of them

page_url = "https://www.playstation.com/pl-pl/ps-plus/games/"
page = requests.get(page_url, params= {'lang' : 'pl-PL'})
soup = BeautifulSoup(page.content, 'html.parser')


games_list = soup.find_all('a', attrs={'module-name' : 'psplusgameslist'})
final_list = [game.text.replace('PS4™ and PS5™', '')
              .replace('PS4', '')
              .replace('PS5', '')
              .replace('(CUSA07377)', '')
              .replace('&','')
              .replace('™', '')
              .replace('®', '')
              .replace('(  )', '').strip() for game in games_list]

#################
# Get links for every game to google its time to beat

how_long_to_beat_links = []
for game in final_list:
            full_url = f'https://www.google.com/search?q={game} how long to beat.com'
            how_long_to_beat_links.append(full_url)

#################
# Get every game's id which is used by How Long to Beat.com

how_long_id_game_list = []

for link in how_long_to_beat_links: 
            url = str(link)
#           headers = {'User-Agent' : 'insert your user agent here'}
            request_result = requests.get(url, headers=headers, cookies= {'CONSENT': 'YES+'})
            soup = BeautifulSoup(request_result.text, 'lxml')
            find_link = soup.find('div', class_='g').find('a')
            print(link)
            
    
            try: 
                get_link = find_link.get('href')
                print(get_link)
            except:
                how_long_id_game_list.append('none')
                continue

            match = re.search('/(\d+)', get_link)
            try: 
                id_game = match.group(1)
            except:
                how_long_id_game_list.append('none')
                continue

            how_long_id_game_list.append(id_game)


            print(f'Adding ID for {link} to the list')
            print(id_game)


#################
# Get time to beat (main, main and sides) for every game


time_to_beat_main = []
time_to_beat_sides = []


for id in how_long_id_game_list:
        full_url = f'https://howlongtobeat.com/game/{id}'
#       headers = {'User-Agent' : 'insert your user agent here'}
        request_howlong = requests.get(full_url, headers=headers)
        second_soup = BeautifulSoup(request_howlong.text, 'lxml')

        if id == 'none':
            time_to_beat_main.append('-')
            time_to_beat_sides.append('-')
        elif id == '38126':
            time_to_beat_main.append('5')
            time_to_beat_sides.append('11')
            continue
        else:
            try:
                find_time = second_soup.find('div', class_= 'GameStats_game_times__KHrRY shadow_shadow').getText()
                print(find_time)
                search = find_time.replace('½', ',5')
                time_main = re.search('Main Story(\S*) Hours', search)
                time_sides = re.search('Sides(\S*) Hours', search)

                time_to_beat_main.append(time_main.group(1))
                time_to_beat_sides.append(time_sides.group(1))

            except:
                time_to_beat_main.append('-')
                time_to_beat_sides.append('-')
                continue

            print(f'Adding time for {id} to the list')


data = {
     'Main Story' : time_to_beat_main,
     'Main and Sides' : time_to_beat_sides
}


#######################
# Get all of the information and combine it into a csv file named "time_to_beat"

df = pd.DataFrame(data)
df.to_csv('time_to_beat.csv', encoding='utf-16', index=False, sep='|')

#######################
# Get basic_info.csv file and time_to_beat.csv and merge them

time = pd.read_csv('time_to_beat.csv', encoding='utf-16', index_col=False, delimiter='|')
info = pd.read_csv('basic_info.csv', encoding='utf-16', index_col=False, delimiter='|')

combine = pd.concat((info,time), axis=1)
combine.to_csv('full_info.csv', encoding='utf-16', index=False, sep='|')
