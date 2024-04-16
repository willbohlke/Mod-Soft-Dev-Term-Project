import wikipediaapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize an empty list to hold the objects
object_list = []

# Read the contents of the file and store each line in the list
with open('fruits.txt', 'r') as file:
    for line in file:
        # Strip any newlines and add to the list
        object_list.append(line.strip())

# Define the object type for better search results (Should be user input at the beginning of the game)
object_type = 'fruit'

wiki_wiki = wikipediaapi.Wikipedia('Guessing Game (https://github.com/willbohlke/Mod-Soft-Dev-Term-Project)', 'en')

def get_descriptions(object_list):
    descriptions = {}
    for object in object_list:
        page = wiki_wiki.page(object)
        if 'Category:Disambiguation pages' in page.categories:
            links = page.links
            # get the link that contains the object_type, else try to select the most relevant link
            for link in links:
                if object_type in link:
                    page = wiki_wiki.page(link)
                    break
                else:
                    # Select the most similar link to object_type
                    most_similar_link = max(links, key=lambda link: object_type in link)
                    page = wiki_wiki.page(most_similar_link)
        section_description = page.section_by_title('Description') or page.section_by_title(object_type)
        if section_description is not None:
            description = section_description.text
        else:
            description = page.summary
        descriptions[object] = description
    return descriptions

def get_similarity(input):
    descriptions_list = get_descriptions(object_list)
    # Create a list of the descriptions and the input string
    texts = list(descriptions.values()) + [input]

    # Convert the texts to TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(texts)

    # Compute the cosine similarity between the input string and the descriptions
    similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1])

    # Create a dictionary of the objects and their similarity to the input string
    similarity_dict = dict(zip(descriptions.keys(), similarities[0]))

    return similarity_dict

# Get the descriptions of all the objects in 'object_list'
descriptions = get_descriptions(object_list)
for object, description in descriptions.items():
    print(f"The description of {object} is: {description}")