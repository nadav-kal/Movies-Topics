import time
import const
import os.path as path
import db.db_builder as db_builder

from api.tmdb import tmdb
from db.repo import movies_repo

if not path.isfile(const.API_PAGE_FILE_NAME):
    with open(const.API_PAGE_FILE_NAME, "w+") as page_file:
        page_file.write("0")

# make api call and store in db every 20 seconds until target
while movies_repo.count_movies() < const.TOTAL_MOVIES:
    db_builder.build_movies_keywords_database(tmdb, movies_repo, 1)
    time.sleep(20)
