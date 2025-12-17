import os 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class MovieRecommender:
    def __init__(self):
        print(" Loading dataset...")
        base_dir = os.path.dirname(__file__)
        csv_path = os.path.join(base_dir, "..", "Dataset", "movies dataset.csv")
        self.movies = pd.read_csv(
          csv_path,
          sep=",",
          quotechar='"',
          escapechar="\\",
          engine="python",
          on_bad_lines="skip"
        )
    
        self.movies["genres"] = self.movies["genres"].fillna(" ")
        self.movies["genres"] = self.movies["genres"].str.replace("|", " ", regex=False)

        vectorizer = CountVectorizer()
        genre_matrix = vectorizer.fit_transform(self.movies["genres"])

        self.similarity = cosine_similarity(genre_matrix)
        print("Dataset Loaded Successfully!")

    def recommend(self, movie_title, n=5):
        if movie_title not in self.movies["title"].values:
            return "Movie not found!"
        
        idx = self.movies[self.movies["title"] == movie_title].index[0]
        scores = list(enumerate(self.similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]

        recommendations = []
        for i, _ in scores:
            recommendations.append(self.movies.iloc[i]["title"])
        return recommendations
if __name__ == "__main__":
        recommender = MovieRecommender()
        print("\nRecommendations:")
        print(recommender.recommend("Toy Story (1995)", n=5))


        
         
       