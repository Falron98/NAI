import csv

import pandas as pd
from recommender import recommend_movie

# Read in data from excell
# Fill "None" if data cell is empty
dataframe1 = pd.read_excel('./data/datasheet.xlsx')
dataframe1.fillna("None", inplace=True)

# Convert to pandas
df = pd.DataFrame(dataframe1)

# Arrays for data
dataset1 = []
movie = []
movies = []

print(df.values[0][3])

for i in range(len(df.values)):
    movies = []
    username = df.values[i][0]
    for j in range(len(df.values[i])):
        if j != 0 and df.values[i][j] != "None" and isinstance(df.values[i][j], str):
            movie = [df.values[i][j], df.values[i][j + 1]]
            movies.append(movie)
    dataset1.append([username, movies])

for t in dataset1:
    print(t)


# Method for choosing username from dataset and checking if its in dataset
def choose_name():
    result = []
    while len(result) != 1:
        name = input("Input name you want to check\n")
        for l in dataset1:
            if name in l[0]:
                result.append(l)
        if len(result) > 1:
            print("Choose full name")
            for i in result:
                print(i[0])
            result = []
    print("Got it")
    print(result)
    return result


# Create csv from excell dataset
def create_csv():
    header = ['username', 'title', 'rating']

    temp_dataset = []
    temp_ratings = []
    for m in range(len(dataset1)):
        for p in range(len(dataset1[m][1])):
            if dataset1[m][1][p][1] != "None":
                temp_ratings.append(dataset1[m][0])
                temp_ratings.append(dataset1[m][1][p][0])
                temp_ratings.append(float((dataset1[m][1][p][1])) / 2)
                temp_dataset.append(temp_ratings)
                temp_ratings = []

    with open('data/data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        writer.writerows(temp_dataset)


# Method for getting all info about chosen movie
def choose_movie(movies_array):
    result = []
    while len(result) != 1:
        name = input("Input name you want to check\n")
        for l in range(len(movies_array)):
            for c in movies_array[l]['movie']:
                print(c)
                if name in c:
                    result.append(c)
        if len(result) > 1:
            print("Choose full name")
            for i in result:
                print(i)
            result = []
    print("Got it")
    print(result[0])
    movies = pd.read_csv('data/movies_data.csv')
    for p in range(len(movies['title'])):
        if result[0] == movies['title'][p]:
            result = movies.iloc[p]
            break
    return result


if __name__ == "__main__":
    create_csv()
    name = choose_name()[0]
    result = recommend_movie(name[0])
    print(choose_movie(result))
