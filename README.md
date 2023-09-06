# My first project used for learning python!

First things first, I realize that the python scripts in this repository have a lot of issues and I am sure there are better ways of achieving the same result. 

That being said, I am quite happy with the result. I learned a few things, visited Stackoverflow numerous times and, perhaps most importantly, achieved the main goals of this project.

## The goals

The following project was created with two goals in mind: familiarizing myself with programming in Python and solving a real problem. The former is obvious, but what was the problem?

There's this service called PS Plus Extra which gives you access to selected games on PS4 and PS5. The list of games can be checked here: https://www.playstation.com/pl-pl/ps-plus/games/

It's a great site, however, it simply lists the games in A-Z order and provides hiperlinks to the PS Store - quite basic when you want to check which games are worth your time and money. 
As a way to learn Python, I decided to create some kind of a tool that would combine the list of games with Opencritic score for each game, its release date and publisher.

## The method

As of now, I have no idea how APIs work and I am not familiar with numerous Python concepts/libraries, so... I went for the most accessible (I think) solution: webscraping.

I visited Stackoverflow quite often, read a bit about BeautifulSoup, Pandas, RegEx, HTML and wrote the following Python program:

Basic_info.py - gathers basic info about each game in PS Extra, if possible (not every game has a score for example), from OpenCritic (https://opencritic.com/) and generates a csv file. It also gets a game's publisher and its release date.

## The result

As a final step, after checking the file manually for potential issues, I decided to generate a Google Looker report with the gathered information. 

It's not perfect, as it was my first time using this service, however, you can check it here:
https://lookerstudio.google.com/embed/reporting/351a79c8-4af9-4cf8-bece-dc0cb2ed545c/page/TwWZD

Using the report you can:
- look for the game that you are interested in (case sensitive)
- filter the games by a publisher (e.g. only display games published by Sony or Ubisoft)
- fitler the games by the time passed since their release date using a slider (e.g. only show games that were released less than two years ago)
- filter by score (e.g. only display games that have a score greater than 80 out of 100)


