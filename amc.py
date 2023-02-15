import re
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup

def get_subtitle(subtitles):
    subtitle_set = set()

    for e in subtitles:
        subtitle = e.text
        if re.search(r"(imax|dolby|reald)", subtitle, re.IGNORECASE):
            subtitle_set.add(subtitle.split(' ')[0])

    return ', '.join(sorted(subtitle_set))

def get_showtime(date):
    url = 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-alderwood-mall-16/showtimes/all/{}/amc-alderwood-mall-16/all'.format(date)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    movies = soup.select('div.ShowtimesByTheatre-film')

    day_of_week = date.strftime('%a')
    
    if day_of_week == 'Thu':
        print("+++++++++++++++++++++++{} {}+++++++++++++++++++++++".format(date, day_of_week))
    else:
        print("-----------------------{} {}-----------------------".format(date, day_of_week))

    for movie in movies:
        title = movie.select_one('h2').text
        subtitle = get_subtitle(movie.select('h4'))
    
        if subtitle:
            print("* {} [{}]".format(title, subtitle))
        else:
            print("  {}".format(title))

# today = date(2023, 2, 14)
today = date.today()
days_ahead = (3 - today.weekday()) % 7 + 14

for i in range(days_ahead):
    date = today + timedelta(days=i)
    get_showtime(date)