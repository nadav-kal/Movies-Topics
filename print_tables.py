# Run this file to print all the tables in the database
from db.repo import movies_repo

print("==== movies table ====")
print(movies_repo.get_all_movies())

print("==== keywords table ====")
print(movies_repo.get_all_keywords())

print("==== movies_keywords table ====")
print(movies_repo.get_all_movies_keywords())

print("==== movies count ====")
print(movies_repo.count_movies())