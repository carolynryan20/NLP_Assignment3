from nltk.parse.generate import generate
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.grammar import CFG
from nltk import ChartParser
from nltk import ngrams
import nltk

def getCFG():
    # make_cfg_rules()
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
        nltk.parse.CoreNLPParser()

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
    f = open("new_cfg.txt", "r")
    grammar_string = f.readlines()
    grammar = CFG.fromstring(grammar_string)
    # for n, sent in enumerate(generate(grammar, n=100), 1):
    #     print('%3d. %s' % (n, ' '.join(sent)))
    return grammar

def parse_original_sentences():
    grammar = construct_cfg_from_string()
    parser = ChartParser(grammar)
    f = open("corpus.txt" , "r")
    f_write = open("parsed_corpus.txt", "w")
    lines = f.readlines()
    count = 1
    working = []
    for line in lines:
        line = line.replace("didnt", "did not")
        print(line)
        s = "Tree {}:\n".format(count)
        sent = word_tokenize(line[:-2])
        for tree in parser.parse(sent):
            s+= str(tree) + "\n\n"
            working.append(count)
            print(tree)
            break
        count += 1
        f_write.write(s)

    # TODO Remove this code once done changing CFG
    s =""
    for i in range(1, 13):
        if i not in working:
            s += str(i) + ", "
    print(s)
    f.close()
    f_write.close()
    print("Parsed form of original corpus sentences using this CFG can be found in parsed_corpus.txt\n")

def clean_sentences(sentence_list):
    for i in range(len(sentence_list)):
        sentence = sentence_list[i][:-2]  # remove .\n
        sentence = sentence.replace('didnt', 'did not') # clean input for improved output
        sentence_list[i] = sentence
    return sentence_list

def get_translation_dict():
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
    f_write = open("translated_sentences.txt", "w")
    english_to_spanish_dict = get_translation_dict()
    sentence_list = clean_sentences(f.readlines())
    translated_sentences = []
    for sentence in sentence_list:
        word_list = sentence.split()
        translated_sentence = ""
        for word in word_list:
            translated_sentence += english_to_spanish_dict[word.lower()] + " "

        translated_sentences.append(translated_sentence)
        f_write.write("English: {}\nSpanish: {}\n\n".format(sentence, translated_sentence))
    f.close()
    f_write.close()
    print("Translated English to Spanish sentences can be found in translated_sentences.txt\n")
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
        print(str(n)+"gram:",found_count / total_tokens)
        return found_count / total_tokens
    else:
        return 0

def calc_sentence_bleu(g_tokens, o_tokens, f_write):
    bleu_num = 0
    blue_denom = 0
    print(" ".join(o_tokens))

    for i in range(1,5):
        precision = calc_precision(g_tokens, o_tokens, i)
        if precision != 0:
            bleu_num += precision
            blue_denom += 1

    if (blue_denom != 0):
        bleu = bleu_num/blue_denom
    else:
        bleu = 0

    sentence = " ".join(o_tokens)
    sentence = sentence[0].upper() + sentence[1:]
    f_write.write("{}\n\t\tBLEU Score: {}\n\n".format(sentence, round(bleu, 5)))
    return bleu

def bleu_score(translated_sentences):
    f = open("google_translations.txt", "r")
    f_write = open("bleu_scores.txt", "w")
    google_translated_sentences = clean_sentences(f.readlines())
    blue_sent = 0
    for i in range(len(translated_sentences)):
        google_sentence = google_translated_sentences[i].lower()
        our_translation = translated_sentences[i]
        g_tokens = google_sentence.split()
        o_tokens = our_translation.split()
        blue_sent += calc_sentence_bleu(g_tokens, o_tokens, f_write)

    blue_avg = blue_sent/12
    print("We have a BLEU score of {} on average for the whole system".format(round(blue_avg,5)))
    f.close()
    f_write.close()
    print("BLEU scores for individual sentences can be seen in bleu_scores.txt")

if __name__ == '__main__':
    getCFG()
    translated_sentences = translate_sentences()
    bleu_score(translated_sentences)