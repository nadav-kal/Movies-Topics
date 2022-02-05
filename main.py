from db.repo import movies_repo
from topic_modeling.builder import TopicsBuilder
import const

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# Function Helpers
def convert_tuples_to_dir(movies_data):
    data = {}
    for (movie_name, keyword_name) in movies_data:
        if not movie_name in data:
            data[movie_name] = []
        data[movie_name].append(keyword_name)
    return data

def filter_movies_data_with_less_than_keywords(movies_data, min_keywords_number):
    new_data = {}
    for movie_name in movies_data.keys():
        if (len(movies_data[movie_name]) >= min_keywords_number):
            new_data[movie_name] = movies_data[movie_name]
    return new_data


# Movies manipulations
movies_data = movies_repo.get_movies_and_their_keywords()
movies_data = convert_tuples_to_dir(movies_data)
movies_data = filter_movies_data_with_less_than_keywords(movies_data, 5)

# Topic Modeling algorithm
topics_builder = TopicsBuilder(movies_data)
topics_builder.run_diagnose(const.NUM_OF_TOPICS, const.NUM_OF_ITER)
prob = topics_builder.get_probablities()

print("======= Topic Modeling Result =======")
print()
print("=== Probabilities Of Topics ===")
print(prob)
print()

# [(movie_name, topic)]
movies_names_topics = topics_builder.get_topics()

# [(movie, topic)]
movies_topics = [(movies_repo.get_movie_by_name(name)[0], topic) for name, topic in movies_names_topics]
movies_topics_sorted_by_popularity = sorted(movies_topics, key=lambda movie_topic: movie_topic[0][4], reverse=True)

def limit_to_at_most_100_movies_per_year(movies_topics):
    movies_by_year = {}
    for movie, topic in movies_topics:
        year = movie[2][:4]
        if not year in movies_by_year:
            movies_by_year[year] = []
        if len(movies_by_year[year]) < 100:
            movies_by_year[year].append((movie, topic))
    return movies_by_year


movies_by_years = limit_to_at_most_100_movies_per_year(movies_topics_sorted_by_popularity)

def split_movies_to_topics(movies_by_years):
    movies_by_years_and_topics = {}
    for year in movies_by_years:
        if not year in movies_by_years_and_topics:
            movies_by_years_and_topics[year] = {}
        for movie, topic in movies_by_years[year]:
            topic = str(topic)
            if not topic in movies_by_years_and_topics[year]:
                movies_by_years_and_topics[year][topic] = []
            movies_by_years_and_topics[year][topic].append(movie[3])
    return movies_by_years_and_topics

movies_by_years_and_topics = split_movies_to_topics(movies_by_years)

movies_and_topics_arr = movies_names_topics
popularity_arr = []

topics_years = set()

for movie_name, topic in movies_and_topics_arr:
    movie = movies_repo.get_movie_by_name(movie_name)
    movie = movie[0]
    year = movie[2]
    year = year[:4]
    topics_years.add((year, topic, movie))
    popularity = movie[4]
    popularity_arr.append(popularity)

i = 0
movies_topics_popularity = []
for movie_topic in movies_and_topics_arr:
    movie_topic_popularity = movie_topic + (popularity_arr[i],)
    i = i+1
    movies_topics_popularity.append(movie_topic_popularity)

sorted_by_popularity = sorted(movies_topics_popularity, key=lambda tup: tup[2])
sorted_by_popularity.reverse()

top_100_popular_movies = sorted_by_popularity[:100]
top_100_popular_movies = [(movie_name, topic) for movie_name, topic, _ in top_100_popular_movies]

print("=== Top 100 Popular movies and their Topics ===")
print(top_100_popular_movies)
print()


# FOR FULL ANALYSIS UNCOMMENT THE FOLLOEING LINES

# print("=== Movies by years and topics ===")
# print(movies_by_years_and_topics)
# print()