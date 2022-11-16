from os.path import exists

import matplotlib.pyplot
import pandas as pd
import tmdbsimple as tmdb
from difflib import SequenceMatcher

import seaborn as sns


# Method in getting recommendation for user in database
def recommend_movie(picked_username):
    # Method for searching movies from users in database
    def search_in_api(ratings):
        # Token required for connecting with database
        tmdb.API_KEY = "5d7af906802f4ffd3fbdb7c1d9b25b68"

        # Arrays for storing searching of movies and series
        movies_arr = []
        tv_series_array = []

        # Call method for searching in database
        movie_tmdb = tmdb.Search()

        # Copy contents of users, movies and ratings
        movies_temp = ratings

        # Loop for searching each title of each movie provided by user
        # in movies database and then adding its infos to array
        for r in ratings['title'].unique():
            response = movie_tmdb.movie(query=r)
            test_matcher_last = 0
            for c in movie_tmdb.results:
                test_matcher = SequenceMatcher(a=r.lower(), b=c['title'].lower()).ratio()
                if test_matcher > 0.8:
                    if test_matcher > test_matcher_last:
                        movie_result = c
                        test_matcher_last = test_matcher
            if test_matcher_last > 0.9:
                print(movie_result['title'] + " == " + r)
                movies_temp = movies_temp[movies_temp.title != r]
                movies_arr.append(movie_result)

        # Loop for searching each title of each movie provided by user
        # in TV series database and then adding its infos to array
        for r in movies_temp['title'].unique():
            response = movie_tmdb.tv(query=r)
            test_matcher_last = 0
            for c in movie_tmdb.results:
                test_matcher = SequenceMatcher(a=r.lower(), b=c['name'].lower()).ratio()
                if test_matcher > 0.8:
                    if test_matcher > test_matcher_last:
                        movie_result = c
                        test_matcher_last = test_matcher
            if test_matcher_last > 0.9:
                print(movie_result['name'] + " == " + r)
                tv_series_array.append(movie_result)

        # Reformatting table of tv_series to match movies table
        test_dataframe = pd.DataFrame(tv_series_array, columns=tv_series_array[0].keys())
        test_dataframe_tv = test_dataframe.rename(
            columns={'first_air_date': 'release_date', 'original_name': 'original_title', 'name': 'title'},
            errors="raise")
        test_dataframe_tv = test_dataframe_tv.drop(columns=['origin_country'])
        test_dataframe = pd.DataFrame(movies_arr, columns=movies_arr[0].keys())

        frames = [test_dataframe, test_dataframe_tv]

        movies = pd.concat(frames)

        return movies

    # Method for creating movie database in csv if doesn't exist
    #
    def create_csv(movies):
        if not exists('data/movies_data.csv'):
            with open('data/movies_data.csv', 'w', encoding='UTF8', newline='') as f:
                pass

        movies.to_csv('data/movies_data.csv', index=False)

    # Read in data about users, movies and ratings
    # if movie database doesn't exist search movies names
    # provided by users and keep them in csv
    ratings = pd.read_csv('data/data.csv')
    if not exists('data/movies_data.csv'):
        movies = search_in_api(ratings)
        create_csv(movies)

    # Read movies_database from csv
    movies = pd.read_csv('data/movies_data.csv')

    print(ratings)
    # Loop for searching movie name chosen by user in movie database
    # the searching with highest similarity ( and similar in more than 90% )
    # is chosen
    for p in movies['title']:
        for t in range(len(ratings['title'])):
            test_matcher = SequenceMatcher(a=p.lower().replace(" ", ""),
                                           b=ratings['title'][t].lower().replace(" ", "")).ratio()
            if test_matcher > 0.9:
                ratings['title'][t] = p

    print(ratings)

    # Merge ratings and movies datasets
    df = pd.merge(ratings, movies, on='title', how='inner')

    # Number of users
    print('The ratings dataset has', df['username'].nunique(), 'unique users')

    # Number of movies
    print('The ratings dataset has', df['title'].nunique(), 'unique movies')

    # Number of ratings
    print('The ratings dataset has', df['rating'].nunique(), 'unique ratings')

    # List of unique ratings
    print('The unique ratings are', sorted(df['rating'].unique()))

    # Aggregate by movie
    agg_ratings = df.groupby('title').agg(mean_rating=('rating', 'mean'),
                                          number_of_ratings=('rating', 'count')).reset_index()

    # Keep the movies with over 1 rating
    agg_ratings_GT100 = agg_ratings[agg_ratings['number_of_ratings'] > 0]
    print(agg_ratings_GT100['title'])

    # Check popular movies
    agg_ratings_GT100.sort_values(by='number_of_ratings', ascending=False).head()

    # Visulization
    sns.jointplot(x='mean_rating', y='number_of_ratings', data=agg_ratings_GT100)

    # Shows visualized graph
    """matplotlib.pyplot.show()"""

    # Merge data
    df_GT100 = pd.merge(df, agg_ratings_GT100[['title']], on='title', how='inner')
    df_GT100.info()

    # Number of users
    print('The ratings dataset has', df_GT100['username'].nunique(), 'unique users')

    # Number of movies
    print('The ratings dataset has', df_GT100['title'].nunique(), 'unique movies')

    # Number of ratings
    print('The ratings dataset has', df_GT100['rating'].nunique(), 'unique ratings')

    # List of unique ratings
    print('The unique ratings are', sorted(df_GT100['rating'].unique()))

    # Setting pd to not limit table
    pd.set_option('display.max_columns', None)
    # Create user-item matrix
    matrix = df_GT100.pivot_table(index='username', columns='title', values='rating')
    print(matrix.head())

    # Normalize user-item matrix
    matrix_norm = matrix.subtract(matrix.mean(axis=1), axis='rows')
    print(matrix_norm.head())

    # User similarity matrix using Pearson correlation
    user_similarity = matrix_norm.T.corr()
    user_similarity.head()

    # Remove picked user ID from the candidate list
    user_similarity.drop(index=picked_username, inplace=True)

    # Take a look at the data
    print(user_similarity)

    # Number of similar users
    n = 5

    # User similarity threashold
    user_similarity_threshold = 0.3

    # Get top n similar users
    similar_users = user_similarity[user_similarity[picked_username] > user_similarity_threshold][
                        picked_username].sort_values(
        ascending=False)[:n]

    # Print out top n similar users
    print(f'The similar users for user {picked_username} are', similar_users)

    # Movies that the target user has watched
    picked_userid_watched = matrix_norm[matrix_norm.index == picked_username].dropna(axis=1, how='all')
    print(picked_userid_watched)

    # Movies that similar users watched. Remove movies that none of the similar users have watched
    similar_user_movies = matrix_norm[matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
    print(similar_user_movies)

    # Remove the watched movie from the movie list
    similar_user_movies.drop(picked_userid_watched.columns, axis=1, inplace=True, errors='ignore')

    # Take a look at the data
    print(similar_user_movies)

    # A dictionary to store item scores
    item_score = {}

    # Loop through items
    for i in similar_user_movies.columns:
        # Get the ratings for movie i
        movie_rating = similar_user_movies[i]
        # Create a variable to store the score
        total = 0
        # Create a variable to store the number of scores
        count = 0
        # Loop through similar users
        for u in similar_users.index:
            # If the movie has rating
            if pd.isna(movie_rating[u]) is False:
                # Score is the sum of user similarity score multiply by the movie rating
                score = similar_users[u] * movie_rating[u]
                # Add the score to the total score for the movie so far
                total += score
                # Add 1 to the count
                count += 1
        # Get the average score for the item
        item_score[i] = total / count

    # Convert dictionary to pandas dataframe
    item_score = pd.DataFrame(item_score.items(), columns=['movie', 'movie_score'])

    # Sort good propositions of movies
    ranked_item_score = item_score.sort_values(by='movie_score', ascending=False)

    # Sort bad propositions of movies
    deranked_item_score = item_score.sort_values(by='movie_score', ascending=True)

    # Select top m movies
    m = 5

    print(ranked_item_score.head(m))
    print(deranked_item_score.head(m))

    return [ranked_item_score.head(m), deranked_item_score.head(m)]
