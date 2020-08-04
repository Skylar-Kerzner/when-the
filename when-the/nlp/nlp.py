import spacy
import random
import json
import urllib.request
# from random_word import RandomWords

# from .core import config as cfg
from core.logging import logger


nlp = spacy.load("en_core_web_md")
# r = RandomWords()



url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
words = json.loads(url.read())

def replace_nouns_with_spacy(phrase: str = ''):
    doc = nlp(phrase)

    s_indices = []
    for idx, token in enumerate(doc):
        if token.text=='s':
            s_indices.append(idx)

    words_list=list()
    for idx, token in enumerate(doc):
        if token.pos_ != 'NOUN':
            if token.text=='s' and idx!=0:
                words_list[-1]+='s'
            else:
                words_list.append(token.text)
        elif token.pos_ == 'NOUN':
            # random_word = r.get_random_words(includePartOfSpeech="noun")
            random_word = random.choice(words)
            words_list.append(random_word)

    phrase = ' '.join(words_list)

    # phrase = phrase.replace(" s ", "s ")

    return phrase

    # Replace subject with anything. Start with replacing nouns

    # Replace verbs, nouns all with some probability


def deplural_question_words(phrase: str = ''):
    # changing spacy words is probably better
    for word in ["who", "what", "when", "where", "why", "how"]:
        phrase = phrase.replace(word+"s", word)
        phrase = phrase.replace(word+"'s", word)
    return phrase


def capitalize_random_word(phrase: str = ''):
    phrase_tokens_list = phrase.split()
    random_index_in_list = random.randrange(len(phrase_tokens_list))

    phrase_tokens_list[random_index_in_list] = \
        phrase_tokens_list[random_index_in_list].upper()

    return ' '.join(phrase_tokens_list)

#a speicfic subset of words in a particular category. Where can i find that. highly charged words. e.g. all nihilist words

while True:
    phrase = input("Input: ")
    #logger.info(f"{'Received message:':<20} {phrase}")
    #phrase = deplural_question_words(phrase)
    #logger.info(f"{'Deplural ?-words:':<20} {phrase}")
    phrase = replace_nouns_with_spacy(phrase)
    #logger.info(f"{'Replaced nouns:':<20} {phrase}")
    phrase = capitalize_random_word(phrase)
    #logger.info(f"{'Random CAPS:':<20} {phrase}")
    print("Output:", phrase)
