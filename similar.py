import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure necessary resources are downloaded
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

class FruitSimilarity:
    def __init__(self, fruits):
        self.fruits = fruits
        self.fruit_definitions = self.get_fruit_definitions()

    def get_fruit_definitions(self):
        fruit_definitions = {}
        for fruit in self.fruits:
            synsets = wn.synsets(fruit)
            for syn in synsets:
                if 'fruit' in syn.definition() or 'fruit' in [lemma.name() for lemma in syn.lemmas()]:
                    fruit_definitions[fruit] = syn.definition()
                    break
        return fruit_definitions

    def calculate_similarity(self, user_description):
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in word_tokenize(user_description.lower()) if word not in stop_words]
        filtered_description = ' '.join(filtered_words)

        descriptions = [filtered_description] + list(self.fruit_definitions.values())
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        similarity_scores = {fruit: score for fruit, score in zip(self.fruit_definitions.keys(), cosine_similarities)}
        sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)

        return sorted_similarity_scores

# example usage

# from similar import FruitSimilarity
# 
# fruits = ["apple", "banana", "orange", "strawberry", "kiwi", "pineapple", "grape", "blueberry", "pear", "peach"]
# fruit_similarity = FruitSimilarity(fruits)
# user_description = "A sweet, red fruit"
# similarity_scores = fruit_similarity.calculate_similarity(user_description)

# print("\nFruits ranked by similarity to your description:")
# for fruit, score in similarity_scores:
#     print(f"{fruit}: {score:.4f}")
