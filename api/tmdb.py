from urllib import request
from urllib import parse
import json

class Tmdb:
    def __init__(self):
        self.DISCOVER_MOVIES_URL = "https://api.themoviedb.org/3/discover/movie?"
        self.GET_MOVIE_URL = "https://api.themoviedb.org/3/movie/"

    def discover_movies(self, from_page=0, pages=1, year=2019):
        pages = [self.get_page(from_page + i, year) for i in range(1, pages + 1)]
        movies = [movie for page in pages for movie in page]
        return movies
        

    def get_keywords(self, movies):
        return [get_keywords(movie.id) for movie in movies]
        
    
    def get_keywords(self, movie_id):
        """ get all keywords from tmdb api of specific movie """
        params = {
            "api_key": "f02638035efb39331179c63490f34c4c"
        }
        params = parse.urlencode(params)
        response = request.urlopen(self.GET_MOVIE_URL + str(movie_id) + "/keywords?" + params)
        keywords = response.read()
        keywords = keywords.decode()
        keywords = json.loads(keywords)
        keywords = keywords["keywords"]
        return keywords

    # def union_keywords(self, movies):
    #     return { keyword for movie in movies for keyword in movie.keywords }

    
    def get_page(self, page, year):
        """ get specific page of popular movies. 
            returns list of Movie objects """
        movies = self.request_movies_from_api(page, year)
        keywords = [self.get_keywords(movie['id']) for movie in movies]
        # movies = [Movie.parse_json(m, k) for m, k in zip(movies, keywords)]
        return movies

    def request_movies_from_api(self, page, year):
        """ make get request to tmdb api.
            returns list in json of popular movies """
        params = self.get_discover_query_params(page, year)
        response = request.urlopen(self.DISCOVER_MOVIES_URL + params)
        movies = response.read()
        movies = movies.decode()
        movies = json.loads(movies)
        movies = movies["results"]
        return movies


    def get_discover_query_params(self, page, year):
        """ make the params for api-get request for tmdb api
            of all popular movies on @page in @year """
        params = {
            "api_key": "f02638035efb39331179c63490f34c4c",
            "language": "en-US",
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "include_video": "false",
            "page": str(page),
            "year": str(year)
        }
        params = parse.urlencode(params)
        return params


tmdb = Tmdb()
# movies = tmdb.discover_movies()
# print("==== page 1 of tmdb movies in 2019 ====") 
# print(movies)

