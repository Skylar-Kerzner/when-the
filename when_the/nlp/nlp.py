import spacy
import random
import urllib.request
import json
# from random_word import RandomWords

# from .core import config as cfg
from when_the.core.logging import logger


nlp = spacy.load("en_core_web_md")
# r = RandomWords()



url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
words = json.loads(url.read())

def replace_nouns_with_spacy(message: str, probability):
    doc = nlp(message)
    tenses_to_replace_words = ['NOUN', 'PROPN', 'VERB']
    words_list=list()
    for idx, token in enumerate(doc):
        if token.pos_ not in tenses_to_replace_words:
            if token.text in ['s','m', 'll'] and idx!=0:
                words_list[-1]+=token.text
            else:
                words_list.append(token.text)
        elif token.pos_ in tenses_to_replace_words:
            # random_word = r.get_random_words(includePartOfSpeech="noun")
            if decide_based_on_probability(probability):
                random_word = random.choice(words)
                words_list.append(random_word)
            else:
                words_list.append(token.text)
    return ' '.join(words_list)

    # Replace subject with anything. Start with replacing nouns

    # Replace verbs, nouns all with some probability

"""
def deplural_question_words(phrase: str = ''):
    # changing spacy words is probably better
    for word in ["who", "what", "when", "where", "why", "how"]:
        phrase = phrase.replace(word+"s", word)
        phrase = phrase.replace(word+"'s", word)
    return phrase
"""

def decide_based_on_probability(probability: float):
    logger.debug("running probability decision...")
    integer = random.randrange(100)
    if (integer/float(100)) < probability:
        logger.debug("probability decided True")
        return True
    else:
        logger.debug("probability decided False")
        return False


def capitalize_random_word(message: str, probability):
    message_tokens_list = message.split()
    if decide_based_on_probability(probability):
        idx = random.randrange(len(message_tokens_list))
        logger.debug(f"Capitalizing at word index {idx}")
        message_tokens_list[idx] = \
        message_tokens_list[idx].upper()
    return ' '.join(message_tokens_list)

def alter_punctuation(message: str, probability):
    message_tokens_list = message.split()
    if decide_based_on_probability(probability):
        idx = random.randrange(len(message_tokens_list))
        logger.debug(f"Altering punctuation after word index {idx}")
        add_punc = random.choice(['.', ',', '!', '?'])
        message_tokens_list[idx] = \
            message_tokens_list[idx] + add_punc
        if add_punc != ',' and idx != len(message_tokens_list)-1:
            message_tokens_list[idx+1] = \
            message_tokens_list[idx+1].title()
    return ' '.join(message_tokens_list)

# Could mimic previous message
def conservative_mimic(message: str, probability):
    message_tokens_list = message.split()
    logger.debug("Doing conservative mimic")
    if decide_based_on_probability(probability):
        for widx, word in enumerate(message_tokens_list):
            if random.choice([True,False]):
                message_tokens_list[widx] = \
                 ''.join([c.upper() if cidx%2==0 else c.lower() for cidx, c in enumerate(word)])
            else:
                message_tokens_list[widx] = \
                 ''.join([c.upper() if cidx%2==1 else c.lower() for cidx, c in enumerate(word)])
    return ' '.join(message_tokens_list)


def alter_message(message: str):
    altered_message = replace_nouns_with_spacy(message, 0.4)
    altered_message = capitalize_random_word(altered_message, 0.25)
    altered_message = alter_punctuation(altered_message, 0.5)
    altered_message = conservative_mimic(altered_message, 0.05)
    return altered_message
#a speicfic subset of words in a particular category. Where can i find that. highly charged words. e.g. all nihilist words

if __name__ == '__main__':
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
