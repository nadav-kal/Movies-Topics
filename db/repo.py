import sqlite3
import atexit
from sqlite3 import Error


class Movie:
    def __init__(self, id, overview, release_date, title, popularity, vote_average, vote_count):
        self.id = id
        self.overview = overview
        self.release_date = release_date
        self.title = title
        self.popularity = popularity
        self.vote_average = vote_average
        self.vote_count = vote_count

class Keyword:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MovieKeyword:
    def __init__(self, movie_id, keyword_id):
        self.movie_id = movie_id
        self.keyword_id = keyword_id


class _Movies:
    def __init__(self, conn):
        self._conn = conn

class _Keywords:
    def __init__(self, conn):
        self.conn = conn

class _Movies_Keywords:
    def __init__(self, conn):
        self.conn = conn

class MovieRepo:
    def __init__(self):
        self._conn = sqlite3.connect("movies.db")
        self.movies = _Movies(self._conn)
        self.keywords = _Keywords(self._conn)
        self.movies_keywords = _Movies_Keywords(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._create_movies_table()
        self._create_keywords_table()
        self._create_movies_keywords_table()
        
    def _create_movies_table(self):
        self._conn.execute(""" 
            CREATE TABLE IF NOT EXISTS movies (
                id              INT         PRIMARY KEY,
                overview        TEXT        NOT_NULL,
                release_date    INT         NOT_NULL,
                title           TEXT        NOT_NULL,
                popularity      REAL        NOT_NULL,
                vote_average    REAL        NOT_NuLL,
                vote_count      INT         NOT_NULL
            );
        """)
    def _create_keywords_table(self):
        self._conn.execute(""" 
            CREATE TABLE IF NOT EXISTS keywords (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT_NULL    
            )
        """)

    def _create_movies_keywords_table(self):
        self._conn.execute(""" 
            CREATE TABLE IF NOT EXISTS movies_keywords (
                movie_id        INT,
                keyword_id      INT,
                PRIMARY KEY(movie_id, keyword_id),
                FOREIGN KEY(movie_id) REFERENCES movies(id),
                FOREIGN KEY(keyword_id) REFERENCES keywords(id)
            )
        """)

    def count_movies(self):
        cur = self._conn.cursor()
        cur.execute("""SELECT COUNT(id) FROM movies""")
        return cur.fetchone()[0]

    def insert_movie(self, movie):
        self._conn.execute("""INSERT OR IGNORE INTO movies (          \
            id,                                             \
            overview,                                       \
            release_date,                                   \
            title,                                          \
            popularity,                                     \
            vote_average,                                   \
            vote_count                                      \
        )                                                   \
        VALUES (?,?,?,?,?,?,?)""",
            [movie.id,
            movie.overview,
            movie.release_date,
            movie.title,
            movie.popularity,
            movie.vote_average,
            movie.vote_count]
        )

    def insert_movies(self, movies):
        for movie in movies:
            self.insert_movie(movie)

    def get_all_movies(self):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM movies")
        return cur.fetchall()


    def insert_keyword(self, keyword):
        self._conn.execute("""INSERT OR IGNORE INTO keywords (        \
            id,                                                       \
            name                                                      \
        )                                                             \
        VALUES (?,?)""",
            [keyword.id,
            keyword.name]
        )

    def insert_keywords(self, keywords):
        for keyword in keywords:
            self.insert_keyword(keyword)

    def get_all_keywords(self):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM keywords")
        return cur.fetchall()


    def insert_movie_keyword(self, movie_keyword):
        self._conn.execute("""INSERT OR IGNORE INTO movies_keywords (   \
            movie_id,                                                   \
            keyword_id                                                  \
        )                                                               \
        VALUES (?,?)""",
            [movie_keyword.movie_id,
            movie_keyword.keyword_id]
        )

    def insert_movies_keywords(self, movies_keywords):
        for movie_keyword in movies_keywords:
            self.insert_movie_keyword(movie_keyword)

    def get_all_movies_keywords(self):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM movies_keywords")
        return cur.fetchall()

    def get_movies_and_their_keywords(self):
        cur = self._conn.cursor()
        cur.execute(
            ''' SELECT 
                    movies.title,
                    keywords.name      
                FROM movies                                 
                    INNER JOIN movies_keywords                    
                        ON movies.id = movies_keywords.movie_id
                    INNER JOIN keywords                                            
                        ON movies_keywords.keyword_id = keywords.id ''')
        return cur.fetchall()

    def get_movie_by_name(self, name):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM movies WHERE title=?",[name])
        return cur.fetchall()

    def get_keywords_by_name(self, name):
        cur  = self._conn.cursor()
        cur.execute(
            ''' SELECT 
                    movies.title,
                    keywords.name      
                FROM movies                                 
                    INNER JOIN movies_keywords                    
                        ON movies.id = movies_keywords.movie_id
                    INNER JOIN keywords                                            
                        ON movies_keywords.keyword_id = keywords.id
                    WHERE movies.title = ?''', [name])
        return cur.fetchall()

movies_repo = MovieRepo()
movies_repo.create_tables()
atexit.register(movies_repo.close)


# # Movies Tests
# mov1 = Movie(1, "overview1", "1954-06-22", "title1", 1, 10, 51)
# mov2 = Movie(2, "overview2", "1954-06-23", "title2", 2, 11, 52)
# mov3 = Movie(3, "overview3", "1954-06-24", "title3", 3, 12, 53)
# mov4 = Movie(4, "overview4", "1954-06-25", "title4", 4, 13, 54)

# movies_repo.insert_movie(mov1)
# movies_repo.insert_movies([mov2, mov3, mov4])
# print("==== movies table ====")
# print(movies_repo.get_all_movies())


# # Keyword Tests
# keyword1 = Keyword(1, "keyword1")
# keyword2 = Keyword(2, "keyword2")
# keyword3 = Keyword(3, "keyword3")
# keyword4 = Keyword(4, "keyword4")

# movies_repo.insert_keyword(keyword1)
# movies_repo.insert_keywords([keyword2, keyword3, keyword4])
# print("==== keywords table ====")
# print(movies_repo.get_all_keywords())


# # Movies_Keywords Tests
# movie_keyword1 = MovieKeyword(1, 1)
# movie_keyword2 = MovieKeyword(1, 2)
# movie_keyword3 = MovieKeyword(2, 1)
# movie_keyword4 = MovieKeyword(3, 1)

# movies_repo.insert_movie_keyword(movie_keyword1)
# movies_repo.insert_movies_keywords([movie_keyword2, movie_keyword3, movie_keyword4])
# print("==== movies_keywords table ====")
# print(movies_repo.get_all_movies_keywords())