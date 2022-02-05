from db.repo import Movie
from db.repo import MovieKeyword
from db.repo import Keyword
import const


def build_movies_keywords_database(tmdb, movies_repo, pages=1):

    from_page = 0
    with open(const.API_PAGE_FILE_NAME, "r") as page_file:
        from_page = int(page_file.readline())

    for i in range(0, pages):
        movies = tmdb.discover_movies(from_page)
        movies = jsonToMovies(movies)
        movies_repo.insert_movies(movies)

        keywords = [tmdb.get_keywords(movie.id) for movie in movies]
        keywords = [jsonToKeywords(keywords_of_movie) for keywords_of_movie in keywords]
        for movie_keywords in keywords:
            movies_repo.insert_keywords(movie_keywords)
    
        movies_keywords = generate_movies_keywords(movies, keywords)
        movies_repo.insert_movies_keywords(movies_keywords)

        from_page += 1

        with open(const.API_PAGE_FILE_NAME, "w") as page_file:
            page_file.write(str(from_page))

    print("movies count: ", movies_repo.count_movies())
    print("api_page: ", from_page)
    print()


def jsonToMovies(json_movies):
    return [make_movie(json_movie) for json_movie in json_movies]

def make_movie(json_movie):
    return Movie (
            json_movie['id'], 
            json_movie['overview'],
            json_movie['release_date'],
            json_movie['title'],
            json_movie['popularity'],
            json_movie['vote_average'],
            json_movie['vote_count'],
    )

def jsonToKeywords(json_keywords):
    return [make_keyword(json_keyword) for json_keyword in json_keywords ]

def make_keyword(json_keyword):
    return Keyword (
            json_keyword['id'], 
            json_keyword['name']
        )

def generate_movies_keywords(movies, keywords):
    movies_keywords = []    

    for movie, keywords in zip(movies, keywords):
        for keyword in keywords:
            movies_keywords.append(make_movie_keyword(movie.id, keyword.id))
    
    return movies_keywords


def make_movie_keyword(movie_id, keyword_id):
    return MovieKeyword(movie_id, keyword_id)





