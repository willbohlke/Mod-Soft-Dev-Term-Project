
import wikipediaapi
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Similarity:
    def __init__(self, object_list, object_type):
        print(f"Initializing Similarity with object_list: {object_list} and object_type: {object_type}")
        self.wiki_wiki = wikipediaapi.Wikipedia('Guessing Bot (https://github.com/willbohlke/Mod-Soft-Dev-Term-Project)', 'en')
        self.object_list = object_list
        self.object_type = object_type
        self.descriptions_cache = {}  # Caching descriptions to avoid repetitive API calls
        if not object_list:
            raise ValueError("Object list is empty.")
        if not object_type:
            raise ValueError("Object type is not specified.")

    def get_descriptions(self):
        descriptions = {}
        for object in self.object_list:
            if object in self.descriptions_cache:
                descriptions[object] = self.descriptions_cache[object]
            else:
                page = self.wiki_wiki.page(object)
                if not page.exists():
                    print(f"No Wikipedia page found for {object}")
                    continue

                description = page.summary
                descriptions[object] = description
                self.descriptions_cache[object] = description  # Store in cache
        return descriptions

    def lemmatize_text(self, text):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        lemmatized_text = " ".join([token.lemma_ for token in doc])
        return lemmatized_text

    def get_guesses(self, input_text):
        descriptions = self.get_descriptions()

        # Create a TfidfVectorizer object
        vectorizer = TfidfVectorizer()

        # Compute TF-IDF values for the input text and the descriptions
        tfidf_matrix = vectorizer.fit_transform([input_text] + list(descriptions.values()))

        # Compute the cosine similarity between the input text and each description
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Get the index of the most similar description
        most_similar_index = cosine_similarities.argmax()

        # Get the object corresponding to the most similar description
        most_similar_object = list(descriptions.keys())[most_similar_index]

        # If the cosine similarity is high enough, return "strong" as the guess strength
        score = cosine_similarities[most_similar_index]

        return most_similar_object, score

# Example usage to debug
# sim = Similarity(['Eiffel Tower', 'Statue of Liberty'], 'landmarks')
# print(sim.get_guesses('A large steel structure in Paris'))
