import wikipediaapi
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class Similarity:
    def __init__(self, object_list, object_type):
        self.wiki_wiki = wikipediaapi.Wikipedia('Guessing Game (https://github.com/willbohlke/Mod-Soft-Dev-Term-Project)', 'en')
        self.object_list = object_list
        self.object_type = object_type

    def get_descriptions(self):
        descriptions = {}
        for object in self.object_list:
            page = self.wiki_wiki.page(object)
            # if not page.exists():
            #     print(f"No Wikipedia page found for {object}")
            #     continue

            # Check if the page is a disambiguation page and get the most relevant link
            if 'Category:Disambiguation pages' in page.categories:
                links = page.links
                for link in links:
                    if self.object_type in link:
                        page = self.wiki_wiki.page(link)
                        break
                    else:
                        most_similar_link = max(links, key=lambda link: self.object_type in link)
                        page = self.wiki_wiki.page(most_similar_link)
            description = ""
            # Get the text from the sections with the most relevant titles
            for section in page.sections:
                if section.title in [self.object_type, 'Characteristics', 'Description', 'Skin']:
                    description += section.text + "\n"
            description += page.summary
            descriptions[object] = description
        return descriptions

    def lemmatize_text(self, text):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        lemmatized_text = " ".join([token.lemma_ for token in doc])
        return lemmatized_text

    
    def get_guesses(self, input):
        print("> Thinking...")
        descriptions_list = self.get_descriptions()

        # Lemmatize descriptions and input
        texts = [self.lemmatize_text(text) for text in descriptions_list.values()] + [self.lemmatize_text(input)]
        
        # Use BERT to convert the texts to vectors
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        vectors = model.encode(texts)
        
        # Compute the cosine similarity between the input vector and the description vectors
        similarities = cosine_similarity([vectors[-1]], vectors[:-1])
        
        similarity_dict = dict(zip(descriptions_list.keys(), similarities[0]))
        
        # Convert scores to percentages and round to 2 decimal places
        similarity_dict = {k: round(v * 100, 2) for k, v in similarity_dict.items()}
        # Filter scores that are above 0
        top_guesses = {k: v for k, v in similarity_dict.items() if v > 0}
        sorted_guesses = sorted(top_guesses.items(), key=lambda x: x[1], reverse=True)
        
        guess_strength = "none"  # Default value
        top_guesses = []  # Default empty list

        if sorted_guesses:
            # Return top 3 guesses
            top_guesses = sorted_guesses[:3]
            score = top_guesses[0][1]
            if score < 50:
                guess_strength = "weak"
            elif score < 70:
                guess_strength = "moderate"
            elif score < 85:
                guess_strength = "strong"
            else:
                guess_strength = "very strong"

        return guess_strength, top_guesses

