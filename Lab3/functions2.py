# Dictionary of movies

movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

def movie_with_high_rating(movie):
    return movie["imdb"] > 5.5

def high_rated(movies):
    return list(filter(movie_with_high_rating, movies))

def with_category(movies, category):
    return list(filter(lambda m: m["category"] == category, movies))

def average_score(movies):
    ratings = list(map(lambda m: m["imdb"], movies))
    return sum(ratings) / len(ratings)

def average_category_score(movies, category):
    ratings = list(map(lambda m: m["imdb"], with_category(movies, category)))
    return sum(ratings) / len(ratings)

category = "Suspense"
print("High rated: ", *high_rated(movies), sep='\n')
print(f"Category {category}: ", *with_category(movies, category), sep='\n')
print("Average score: ", average_score(movies))
print(f"Average score with category {category}: ", average_category_score(movies, category))
