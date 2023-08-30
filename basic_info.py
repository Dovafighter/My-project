import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#################
# Get names of games that are currently available in PS Extra and make a list out of them

page_url = "https://www.playstation.com/pl-pl/ps-plus/games/"
page = requests.get(page_url, params= {'lang' : 'pl-PL'})
soup = BeautifulSoup(page.content, 'html.parser')


games_list = soup.find_all('a', attrs={'module-name' : 'PS Plus Games List'})
final_list = [game.text.replace('PS4™ and PS5™', '')
              .replace('PS4', '')
              .replace('PS5', '')
              .replace('(CUSA07377)', '')
              .replace('&','')
              .replace('™', '')
              .replace('®', '')
              .replace('(  )', '')
              .strip() for game in games_list]

unique_games = set(final_list)
unique_final_list = sorted(list(unique_games), key=str.lower)

print(final_list)
print('Second list')
print(unique_final_list)

################################
# Create a google search link (game's name + "opencritic") for every game in the list
# and add it to a new list

links = []

for game in final_list:
    search = f'{game} opencritic'
    full_url = f'https://www.google.com/search?q={search}'
    links.append(full_url)

###################################
# Use every google search link in the list named "links" and get the game's 
# ID used by opencritic


id_game_list = []

for link in links:
    if link == 'https://www.google.com/search?q=Assassin’s Creed Chronicles: India opencritic':
        id_game_list.append('1613')
        continue
    elif link == 'https://www.google.com/search?q=Hotline Miami 2: Wrong Number opencritic':
        id_game_list.append('87')
        continue
    elif link == 'https://www.google.com/search?q=How to Survive 2 opencritic':
        id_game_list.append('3811')
        continue
    elif link == 'https://www.google.com/search?q=Lost Words: Beyond the Page opencritic':
        id_game_list.append('9230')
        continue
    elif link == 'https://www.google.com/search?q=The Talos Principle: Deluxe Edition opencritic':
        id_game_list.append('613')
        continue
    elif link == 'https://www.google.com/search?q=Townsmen - A Kingdom Rebuilt opencritic':
        id_game_list.append('7350')
        continue
    elif link == 'https://www.google.com/search?q=Pillars of Eternity II: Deadfire - Ultimate Edition opencritic':
        id_game_list.append('7350')
        continue
    elif link == 'https://www.google.com/search?q=Rock of Ages 3: Make  Break opencritic':
        id_game_list.append('9260')
        continue
    elif link == 'https://www.google.com/search?q=Power Rangers: Battle For The Grid opencritic':
        id_game_list.append('7508')
        continue
    else:      
        url = str(link)
#        headers = {'User-Agent' : 'insert your browser user agent here'}
        request_result = requests.get(url, headers=headers, cookies= {'CONSENT': 'YES+'})
        soup = BeautifulSoup(request_result.text, 'lxml')
        find_link = soup.find('div', class_='eFM0qc BCF2pd iUh30').find('a', class_='fl iUh30')

        try: 
            get_link = find_link.get('href')
        except:
            id_game_list.append('none')
            continue

        match = re.search('/(\d+)/', get_link)
        try: 
            id_game = match.group(1)
        except:
            id_game_list.append('none')
            continue

        id_game_list.append(id_game)


        print(f'Adding ID for {link} to the list')

print(id_game_list)


###############################################
# Using the extracted IDs used by opencritic, get the game's info 
# (rating, release date, publisher) from opencritic and add them to new lists


rating_list = []
publisher_list = []
release_date_list = []

replacements = [
    ('Jan', '01'),
    ('Feb', '02'),
    ('Mar', '03'),
    ('Apr', '04'),
    ('May', '05'),
    ('Jun', '06'),
    ('Jul', '07'),
    ('Aug', '08'),
    ('Sep', '09'),
    ('Oct', '10'),
    ('Nov', '11'),
    ('Dec', '12')
]

for id in id_game_list:
    full_url = f'https://opencritic.com/game/{id}/placeholder'
#    headers = {'User-Agent' : 'insert your browser user agent here'}
    request_opencritic = requests.get(full_url, headers=headers)
    

    second_soup = BeautifulSoup(request_opencritic.text, 'lxml')
    if id == 'none':
        rating_list.append('-')
        publisher_list.append('-')
        release_date_list.append('-')
        continue
    else:
        try:
            find_score = second_soup.find('div', class_='inner-orb').getText()
            find_date = second_soup.find('div', class_='platforms').getText()
            find_publisher = second_soup.find('div', class_='companies').getText()
            date = re.search('(.*) (\d+), (\d+) -', find_date)

            if 'Ubisoft' in find_publisher:
                name_publisher = 'Ubisoft'
            elif 'Sony' in find_publisher:
                name_publisher = 'Sony'
            elif 'Naughty Dog' in find_publisher:
                name_publisher = 'Sony'
            elif 'XSEED Games' in find_publisher:
                name_publisher = 'Xseed'
            elif 'PlayStation' in find_publisher:
                name_publisher = 'Sony'
            elif 'BANDAI NAMCO Entertainment' in find_publisher:
                name_publisher = 'Bandai Namco Games'
            elif 'CAPCOM Co.' in find_publisher:
                name_publisher = 'Capcom'
            elif 'Paradox Development Studio' in find_publisher:
                name_publisher = 'Paradox Interactive'
            elif ',' in find_publisher:
                publisher = re.search('(^.*?),', find_publisher)
                name_publisher = publisher.group(1)
            else:
                publisher = re.search('(.*)', find_publisher)
                name_publisher = publisher.group(1)




            month = date.group(1).strip()
            for old, new in replacements:
                month = month.replace(old, new)

            day = date.group(2)
            if len(day) == 1:
                day = f'0{date.group(2)}'
            else:
                day = date.group(2)
            year = date.group(3)
            formatted_date = f'{year}-{month}-{day}'

        except:
            rating_list.append('-')
            publisher_list.append('-')
            release_date_list.append('-')
            continue

        print(f'Adding score for {id} to the list')
        rating_list.append(find_score)
        publisher_list.append(name_publisher)
        release_date_list.append(formatted_date)
        print(formatted_date)
        print(name_publisher)


data = {
    'Game' : final_list,
    'Score' : rating_list,
    'Publisher' : publisher_list,
    'Release' : release_date_list
}

#######################
# Get all of the information and combine it into a csv file named "basic_info"

df = pd.DataFrame(data)
df.drop_duplicates()
df.to_csv('basic_info.csv', encoding='utf-16', index=False, sep='|')
