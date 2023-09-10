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
final_list = [game.text
              .replace('PS4™ and PS5™', '')
              .replace('PS4', '')
              .replace('PS5', '')
              .replace('(CUSA07377)', '')
              .replace('&','')
              .replace('™', '')
              .replace('®', '')
              .replace('(  )', '')
              .strip() 
              for game in games_list]

unique_final_list = sorted(final_list[:25])

print(final_list)
print('Second list')
print(unique_final_list)

##############
# Connect to OpenCritic API for a game's id

id_game_list = []
url = "https://opencritic-api.p.rapidapi.com/game/search"

for game in unique_final_list:
    querystring = {"criteria": game}
    headers = {
        "X-RapidAPI-Key": "for key and host you can register here: https://rapidapi.com/opencritic-opencritic-default/api/opencritic-api",
        "X-RapidAPI-Host": "for key and host you can register here: https://rapidapi.com/opencritic-opencritic-default/api/opencritic-api"
    }

    response = requests.get(url, headers=headers, params=querystring)

    info = response.json()

    print(info)

    dictionary = info[0]
    id = dictionary['id']
    print(f"ID for {game} is: {id}")
    id_game_list.append(id)

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
    headers = {'User-Agent' : 'insert your user agent here'}
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
        else:
            print(f'Adding score, publisher and release date for {id} to the list')
            rating_list.append(find_score)
            publisher_list.append(name_publisher)
            release_date_list.append(formatted_date)
            print(formatted_date)
            print(name_publisher)


data = {
    'Game' : unique_final_list,
    'Score' : rating_list,
    'Publisher' : publisher_list,
    'Release' : release_date_list
}

#######################
# Get all of the information and combine it into a csv file named "basic_info"

df = pd.DataFrame(data)
df.drop_duplicates()
df.to_csv('basic_info_api.csv', encoding='utf-16', index=False, sep='|')
