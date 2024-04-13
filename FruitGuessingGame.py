import spacy
import wikipediaapi
import re

# Load the spaCy model with word vectors
nlp = spacy.load('en_core_web_md')

# list of fruits
fruits = [
    "Apple", "Banana", "Orange", "Strawberry", "Mango", "Grape", "Pineapple", "Avocado",
    "Blueberry", "Lemon", "Watermelon", "Cherry", "Tomato", "Kiwi", "Peach", "Raspberry",
    "Nectarine", "Grapefruit", "Blackberry", "Melon", "Plum", "Pear", "Lime", "Cranberry",
    "Papaya", "Fig", "Passionfruit", "Tangerine", "Pomegranate", "Coconut", "Lychee", "Guava",
    "Clementine", "Date (fruit)", "Dragonfruit", "Durian", "Star fruit", "Apricot", "Tangelo"
]

# Function to fetch fruit info from Wikipedia
def fetch_fruit_info(fruits):
    user_agent = "Fruit Guessing Chatbot (https://github.com/willbohlke/Mod-Soft-Dev-Term-Project.git)"
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
    
    fruit_summaries = {}
    for fruit in fruits:
        page = wiki_wiki.page(fruit)
        if page.exists():
            fruit_summaries[page.title] = page.summary
    
    return fruit_summaries

# Function to extract keywords from the fruit summaries
def extract_keywords(fruit_summaries):
    keywords = {}
    number_pattern = re.compile(r'\d')  # Regex pattern to detect digits for entry removal

    for fruit, summary in fruit_summaries.items():
        # Process the summary text
        doc = nlp(summary)
        # Extract adjectives, and named entities as keywords
        extracted_keywords = [token.text for token in doc if token.pos_ == 'ADJ' and not number_pattern.search(token.text)]
        extracted_keywords += [ent.text for ent in doc.ents if not number_pattern.search(ent.text)]
        keywords[fruit] = list(set(extracted_keywords))  # Use set to remove duplicates
    return keywords

# Driver code
fruit_summaries = fetch_fruit_info(fruits)
keywords = extract_keywords(fruit_summaries)

print("Keywords for Watermelon:")
for keyword in keywords["Watermelon"]:
    print(keyword)
