from nltk.parse.generate import generate
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.grammar import CFG
from nltk import ChartParser

start_possibles = []
rules = {}

def main():
    f = open("corpus.txt", "r")
    for line in f.readlines():
        word_tokens = word_tokenize(line)
        line_pos = pos_tag(word_tokens)

        start = ""
        for _, tag in line_pos:
            start += tag + " "
        start_possibles.append(start[:-3])

        for word, tag in line_pos:
            if not tag == "." :
                word = "'"+word+"'"
                if not rules.get(tag):
                    rules[tag] = [word]
                elif word not in rules.get(tag):
                    rules[tag].append(word)

    f.close()

    # construct_cfg()
    parse()

def construct_cfg():
    grammar_string = "S -> "
    for start_pos in start_possibles:
        grammar_string += start_pos + " | "
    grammar_string = grammar_string[:-2] + "\n"

    for key, value_list in rules.items():
        grammar_string += key + " -> "
        for item in value_list:
            grammar_string += item + " | "
        grammar_string = grammar_string[:-2] + "\n"

    print(grammar_string)

    grammar = CFG.fromstring(grammar_string)
    # for n, sent in enumerate(generate(grammar), 1):
    #     print('%6d. %s' % (n, ' '.join(sent)))
    return grammar

def parse():
    parser = ChartParser(construct_cfg())
    sent = word_tokenize("I just spent 7 hours playing with fonts")
    for tree in parser.parse(sent):
        print(tree)

def clean_sentences(sentence_list):
    for i in range(len(sentence_list)):
        sentence = sentence_list[i][:-2]  # remove .\n
        sentence = sentence.replace('didnt', 'did not')
        sentence_list[i] = sentence
    return sentence_list

def get_translations():
    f = open("translations.txt", "r")
    english_to_spanish_dict = {}
    for line in f.readlines():
        line = line.lower()
        english_spanish = line.split(":")
        english = english_spanish[0]
        spanish = english_spanish[1][:-1] # remove \n
        english_to_spanish_dict[english] = spanish

    f.close()
    return english_to_spanish_dict

def translate_sentences():
    f = open("corpus.txt", "r")
    english_to_spanish_dict = get_translations()
    sentence_list = clean_sentences(f.readlines())
    translated_sentences = []
    for sentence in sentence_list:
        word_list = sentence.split()
        translated_sentence = ""
        for word in word_list:
            translated_sentence += english_to_spanish_dict[word.lower()] + " "

        translated_sentences.append(translated_sentence)
        print("\nEnglish:", sentence)
        print("Spanish:", translated_sentence)
    f.close()
    return translated_sentences

def calc_bleu_score(translated_sentences):
    f = open("google_translations.txt", "r")
    google_translated_sentences = clean_sentences(f.readlines())
    for i in range(len(translated_sentences)):
        google_sentence = google_translated_sentences[i]
        our_translation = translated_sentences[i]
        print(google_sentence, "\n"+our_translation)

    f.close()



if __name__ == '__main__':
    which_to_run = input("Enter either CFG or T: ").upper()
    while which_to_run != "CFG" and which_to_run != "T":
        which_to_run = input("Enter either CFG or T (for translate): ").upper()
    if which_to_run == "CFG":
        main()
    elif which_to_run == "T":
        translated_sentences = translate_sentences()
        calc_bleu_score(translated_sentences)