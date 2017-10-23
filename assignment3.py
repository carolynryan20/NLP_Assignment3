from nltk.parse.generate import generate
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.grammar import CFG
from nltk import ChartParser
from nltk import ngrams



def getCFG():
    construct_cfg_from_string()
    parse_original_sentences()


def make_cfg_rules():
    '''
    Tokenizes words, no longer in use but helped a ton with the grammar.txt file rule construction
    Looped over words in corpus and made a mapping of POS -> word, with S being the POS of all original sentences
    :return: None
    '''
    start_possibles = []
    rules = {}
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

def construct_cfg_from_string():
    f = open("grammar.txt", "r")
    grammar_string = f.readlines()
    grammar = CFG.fromstring(grammar_string)
    #TODO Have infinite grammar structure.....
    # for n, sent in enumerate(generate(grammar, n=100), 1):
    #     print('%3d. %s' % (n, ' '.join(sent)))
    return grammar

def parse_original_sentences():
    grammar = construct_cfg_from_string()
    parser = ChartParser(grammar)
    f = open("corpus.txt" , "r")
    lines = f.readlines()
    count = 1
    working = []
    for line in lines:
        print("Tree {}:".format(count))
        sent = word_tokenize(line[:-2])
        for tree in parser.parse(sent):
            print(tree)
            working.append(count)
            break
        count += 1
    s =""
    for i in range(1, 13):
        if i not in working:
            s += str(i) + ", "
    print(s)

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

def calc_precision(g_tokens, o_tokens, n):
    g_ngrams = list(ngrams(g_tokens, n))
    o_ngrams = list(ngrams(o_tokens, n))
    found_count = 0
    total_tokens = len(o_ngrams)
    for o_ngram in o_ngrams:
        for g_ngram in g_ngrams:
            if g_ngram == o_ngram:
                found_count += 1
                break

    if total_tokens != 0:
        return found_count / total_tokens
    else:
        return 0

def calc_sentence_bleu(g_tokens, o_tokens):
    bleu_num = 0
    blue_denom = 0
    for i in range(1,5):
        precision = calc_precision(g_tokens, o_tokens, i)
        if precision != 0:
            bleu_num += precision
            blue_denom += 1

    if (blue_denom != 0):
        bleu = bleu_num/blue_denom
    else:
        bleu = 0

    print("BLEU Score: {} for {}".format(bleu, " ".join(o_tokens)))
    return bleu

    # UNIGRAM
    found_count = 0
    total_tokens = len(o_tokens)
    for gtoken in g_tokens:
        for otoken in o_tokens:
            if gtoken == otoken:
                found_count += 1
                break
    unigram_precision = found_count/total_tokens



def bleu_score(translated_sentences):
    f = open("google_translations.txt", "r")
    google_translated_sentences = clean_sentences(f.readlines())
    for i in range(len(translated_sentences)):
        google_sentence = google_translated_sentences[i].lower()
        our_translation = translated_sentences[i]
        g_tokens = google_sentence.split()
        o_tokens = our_translation.split()
        calc_sentence_bleu(g_tokens, o_tokens)

    f.close()



if __name__ == '__main__':
    getCFG()
    # translated_sentences = translate_sentences()
    # print()
    # bleu_score(translated_sentences)