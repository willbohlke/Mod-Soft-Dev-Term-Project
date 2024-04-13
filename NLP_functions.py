import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure necessary resources are downloaded
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('stopwords')

#initialize the list of fruits
fruits = ["apple", "banana", "orange", "strawberry", "kiwi", "pineapple", "grape", "blueberry", "pear", "peach"]

def get_fruit_definitions(fruits):
    fruit_definitions = {}

    for fruit in fruits:
        synsets = wn.synsets(fruit)
        for syn in synsets:
            if 'fruit' in syn.definition() or 'fruit' in [lemma.name() for lemma in syn.lemmas()]:
                fruit_definitions[fruit] = syn.definition()
                break

    return fruit_definitions

def calculate_similarity(user_description, fruit_definitions):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in word_tokenize(user_description.lower()) if word not in stop_words]
    filtered_description = ' '.join(filtered_words)

    descriptions = [filtered_description] + list(fruit_definitions.values())
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    similarity_scores = {fruit: score for fruit, score in zip(fruit_definitions.keys(), cosine_similarities)}
    sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)

    return sorted_similarity_scores

def main():
    fruit_definitions = get_fruit_definitions(fruits)
    user_description = input("Describe a fruit: ")
    similarity_scores = calculate_similarity(user_description, fruit_definitions)

    print("\nFruits ranked by similarity to your description:")
    for fruit, score in similarity_scores:
        print(f"{fruit}: {score:.4f}")

if __name__ == "__main__":
    main()
