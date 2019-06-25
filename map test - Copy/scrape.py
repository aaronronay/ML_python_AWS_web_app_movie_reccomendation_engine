from bs4 import BeautifulSoup
import requests
import json
from splinter import Browser
import datetime
from config import gkey


def theater_scrape():
    executable_path = {'executable_path': 'static/webdriver/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    zipcode = 44107
    movie_date = datetime.datetime.today().strftime('%Y-%m-%d')
    url = (
        "https://www.fandango.com/{0}_movietimes?mode=general&q={0}&date={1}").format(zipcode, movie_date)
    print("The URL being scraped is")
    print(url)
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    showtimes = soup.find('div', class_='fd-showtimes')
    theaters = showtimes.find_all('li', class_='fd-theater')
    #create empty dictionary
    theater_data = []
    #Find theater_names, theater locations, movies, and showtimes.
    theater_names = []
    theater_locations = []
    theaters_movies = []
    #for i in range(0, len(theaters)):
    for i in range(0,1): #for testing purposes
        theater_name = theaters[i].find('a', class_='light').text
        theater_names.append(theater_name)
        theaterlocation = theaters[i].find(
            'div', class_='fd-theater__address-wrap').text
        theater_location = ' '.join(theaterlocation.rstrip().split())
        theater_locations.append(theater_location)
        movies = theaters[i].find_all('li', class_='fd-movie')
        theater_movies = []
        movies_titles = []
        movies_showtimes = []
        movies_posters = []
        target = theater_location
        # Build the endpoint URL
        target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
        'address={0}&key={1}').format(target, gkey)
        # Run a request to endpoint and convert result to json
        geo_data = requests.get(target_url).json()
        lat = geo_data["results"][0]["geometry"]["location"]["lat"]
        lng = geo_data["results"][0]["geometry"]["location"]["lng"]
        for k in range(0, len(movies)):
            if movies[k].find('a', class_='dark'):
                movie_title = movies[k].find('a', class_='dark').text
            else:
                movie_title = movies[k].find('a', class_='dark')
            movies_titles.append(movie_title)
            if movies[k].find('img'):
                movie_poster = movies[k].find('img')['src']
            else:
                movie_poster = movies[k].find('img')
            movies_posters.append(movie_poster)
            movie_showtimes = []
            if movies[k].find_all('a', class_='showtime-btn--available'):
                numshows = movies[k].find_all(
                    'a', class_='showtime-btn--available')
            else:
                numshows = movies[k].find_all(
                    'span', class_='showtime-btn--non-ticketing')
            for j in range(0, len(numshows)):
                showtime = numshows[j].text
                movie_showtimes.append(showtime)
            movies_showtimes.append(movie_showtimes)
            theater_movies.append(
                {'Title': movies_titles[k], 'Showtimes': movies_showtimes[k], 'Poster_URL': movies_posters[k]})
        theaters_movies.append(theater_movies)
        theater_data.append(
            {'Name': theater_names[i], 'Address': theater_locations[i], 'lat': lat, 'lng': lng, 'Movies': theaters_movies[i]})
    # with open('static/result' + str(location) + '.json', 'w') as fp:
    #     json.dump(theater_data, fp)
    return(theater_data)


if __name__ == "__main__":
    print(theater_scrape())
