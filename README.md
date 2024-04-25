# Mod-Soft-Dev-Term-Project

This is our guessing program based on the original ELIZA script. The user can load .txt files into /Game Modes containing a list of whatever they want the program to guess. The program will then use API's and NLP to retrieve info related to the items listed and then formulate guesses based on what the user has described. 

## Requirements (Run these in the terminal of your environment before using):

```python
pip install unittest #For unit testing
pip install wikipedia-api #This api fetches descriptions of the objects loaded from the .txt file
pip install -U scikit-learn #Used for NLP to calculate cosign similarity
pip install spacy #Provides lemmatization in the NLP process
python -m spacy download en_core_web_sm #Try replacing 'sm' with 'md' or 'lg' for more accurate guesses. However, they are a larger downloads.
pip install sentence-transformers #to use BERT language processing
pip install PyQt5
```

## How to play:
1. install the modules listed above
2. run gui2.py and the game will load!
