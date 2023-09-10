import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#################
    # Get names of games that are currently available in PS Extra and make a list out of them

def get_playstations_games():
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
    print(final_list)
    unique_final_list = sorted(final_list)
    return unique_final_list

################################
# Create a google search link (game's name + "opencritic") for every game in the list
# and add it to a newly created list

def create_opencritic_links(list):
    links = []
    for game in list:
        search = f"{game} 'opencritic.com'"
        full_url = f"https://www.google.com/search?q={search}"
        links.append(full_url)
    return links

###########
# Get opencritic id for every googled game

def get_opencritic_id_for_game(opencritic_links):
    id_game_list = []
    for link in opencritic_links:    
            url = str(link)
            headers = {'User-Agent' : 'insert your user agent here'}
            request_result = requests.get(url, headers=headers, cookies= {'CONSENT': 'YES+'})
            soup = BeautifulSoup(request_result.text, 'lxml')
            find_link = soup.find('div', class_='eFM0qc BCF2pd iUh30').find('a', class_='fl iUh30')
            try: 
                get_link = find_link.get('href')
            except:
                id_game_list.append('none')
                continue
            else:
                match = re.search('/(\d+)/', get_link)
                try: 
                    id_game = match.group(1)
                except:
                    id_game_list.append('none')
                    continue
                else:
                    id_game_list.append(id_game)
                    print(f'Adding ID for {link} to the list')
    print(id_game_list)
    return id_game_list



###############################################
# Using the extracted IDs used by opencritic, get the game's info 
# (rating, release date, publisher) from opencritic and add them to new lists

def get_rating_publisher_and_release_date(id_game_list):
    rating_list = []
    publisher_list = []
    release_date_list = []

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
                print(f'Adding score for {id} to the list')
                rating_list.append(find_score)
                publisher_list.append(name_publisher)
                release_date_list.append(formatted_date)
                print(formatted_date)
                print(name_publisher)
    details = [rating_list, publisher_list, release_date_list]
    return details

games = get_playstations_games()
links = create_opencritic_links(games)
ids_of_games = get_opencritic_id_for_game(links)
list_of_details = get_rating_publisher_and_release_date(ids_of_games)

data = {
        'Game' : games,
        'Score' : list_of_details[0],
        'Publisher' : list_of_details[1],
        'Release' : list_of_details[2]
}

    #######################
    # Get all of the information and combine it into a csv file named "basic_info"

df = pd.DataFrame(data)
df.drop_duplicates()
df.to_csv('basic_info.csv', encoding='utf-16', index=False, sep='|')

    
