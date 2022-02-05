# Movies Topics with Topic Modeling

This project was made for the course "Topics in Digital Humanities"  by **Aviv Elkayam** and **Nadav Kalimi**.

## Description

### Goal

This project goal was to find if there is a connection between the topics of the movies as they are reflected by the movies keywords, to the success of the movies. 

### The Process

We used TMDB API to get 7,000 movies and their related keywords, then we stored the them in a relational database.

After that we took all the movies and their related keywords from our database and filtered them. This step was done to make the Topic Modeling algorithm results be more accurate.  

Then, we ran the topic modeling algorithm on our filtered data and tried to match a name for each topic we get. this process was made over and over again (with different topics modeling parameters) until we found the names that fits our results.    


## Usage

1. Change the constant ```TOTAL MOVIES``` in ```const.py``` to match the number of movies you want to load.
2. Run the python script ```movies_loader.py```. 
3. Change the constant ```NUM_OF_TOPICS``` and ```NUM_OF_ITER``` to match your topics modeling algorithm parameters that you want.
4. Run the python script ```main.py``` to run the topic modeling algorithm. The results will be printed to the screen.

**Notice:**  The 2nd step is making a requests to the TMDB API. Each request get 20 movies and their keywords. Each request is followed by 20 seconds sleep in order to prevent API overload.

## Full Analysis 

Uncomment these lines in ```main.py``` to see all the movies sorted by their topics and their years

```python
print("=== Movies by years and topics ===")
print(movies_by_years_and_topics)
print()
```

## Results
### Top popular movies by their topics 
![alt text](https://i.ibb.co/QjHsKLk/100.png)

### Distribution of the popular movies by their topics and their years
![alt text](https://i.ibb.co/GCGStH6/image.png)



