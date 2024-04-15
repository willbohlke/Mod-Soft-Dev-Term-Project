import string
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertModel, BertTokenizer

class FruitSimilarity:
    def __init__(self, fruit_list):
        self.nlp = spacy.load('en_core_web_lg')
        self.fruit_definitions = self.get_fruit_definitions(fruit_list)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
    def get_fruit_definitions(self, fruit_list):
        fruit_definitions = {}
        for fruit in fruit_list:
            synsets = wordnet.synsets(fruit)
            if synsets:
                fruit_definitions[fruit] = synsets[0].definition()
        return fruit_definitions

    def preprocess_text(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        doc = self.nlp(text)
        lemmatized_words = [self.lemmatizer.lemmatize(token.text, pos='v') for token in doc if token.text not in self.stop_words]
        return ' '.join(lemmatized_words)
    
    def get_bert_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = self.model(**inputs)
        # Get the embeddings for the CLS token (index 0)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        return cls_embedding

    def calculate_similarity(self, user_description):
        # Preprocess user description
        filtered_user_description = self.preprocess_text(user_description)
        # Preprocess all fruit definitions
        filtered_definitions = {fruit: self.preprocess_text(definition) for fruit, definition in self.fruit_definitions.items()}

        # Create document corpus and calculate TF-IDF matrix
        corpus = [filtered_user_description] + list(filtered_definitions.values())
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        # Calculate cosine similarity for TF-IDF as initial filter
        initial_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        top_indices = initial_scores.argsort()[0][-5:]  # Get top 5 indices for detailed BERT analysis
        
        # Calculate detailed similarity using BERT for top 5 TF-IDF results
        user_emb = self.get_bert_embeddings(filtered_user_description)
        bert_scores = []
        for index in top_indices:
            fruit_name = list(filtered_definitions.keys())[index]
            fruit_emb = self.get_bert_embeddings(filtered_definitions[fruit_name])
            cos_sim = cosine_similarity(user_emb.detach().numpy(), fruit_emb.detach().numpy())[0][0]
            bert_scores.append((fruit_name, cos_sim))
        
        # Final sorting of results
        sorted_similarity_scores = sorted(bert_scores, key=lambda item: item[1], reverse=True)
        
        return sorted_similarity_scores
