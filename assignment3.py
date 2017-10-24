from nltk.tokenize import word_tokenize
from nltk.grammar import CFG
from nltk import ChartParser
from nltk import ngrams
### Written by Carolyn Ryan
### Uses defined CFG to parse sentences
### Uses English word=>Spanish word translation to translate sentences
### Calculates BLEU score of the translated sentences

def construct_cfg_from_string():
    '''
    Reads CFG rules from cfg.txt
    Uses nltk to make a grammar from the given rules
    :return: CFG (nltk.grammar.CFG)
    '''
    f = open("cfg.txt", "r")
    grammar_string = f.readlines()
    grammar = CFG.fromstring(grammar_string)
    f.close()
    return grammar

def parse_original_sentences(grammar):
    '''
    Uses given grammar to parse sentences from the file corpus.txt
    Writes the parse trees of each sentence in parsed_corpus.txt
    :param grammar: A context free grammar in the form of nltk.grammar.CFG
    :return: None (Output in parsed_corpus.txt)
    '''
    parser = ChartParser(grammar)
    f = open("corpus.txt" , "r")
    f_write = open("parsed_corpus.txt", "w")
    lines = f.readlines()
    count = 1
    working = []
    for line in lines:
        line = line.replace("didnt", "did not")
        s = "Tree {}:\n".format(count)
        sent = word_tokenize(line[:-2])
        for tree in parser.parse(sent):
            s+= str(tree) + "\n\n"
            working.append(count)
            break
        count += 1
        f_write.write(s)

    f.close()
    f_write.close()
    print("Parsed form of original corpus sentences using this CFG can be found in parsed_corpus.txt\n")

def clean_sentences(sentence_list):
    '''
    Cleans sentences by removing periods and new line characters
    Gets rid of known contractions in the corpus (in this case replaces didn't with did not)
    :param sentence_list: A list of sentences
    :return: Clean list of sentences
    '''
    for i in range(len(sentence_list)):
        sentence = sentence_list[i][:-2]  # remove .\n
        sentence = sentence.replace('didnt', 'did not') # clean input for improved output
        sentence_list[i] = sentence
    return sentence_list

def get_translation_dict():
    '''
    Reads direct translations from file translations.txt and makes an English to Spanish dictionary
    where the key is the word in English and the value is that word translated to Spanish
    :return: English to Spanish dict
    '''
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

def translate_sentences(english_to_spanish_dict):
    '''
    Reads sentences from corpus.txt, uses English to Spanish dictionary to translate sentences
    Writes translated sentences to file translated_sentences.txt
    :param english_to_spanish_dict: An English to Spanish dictionary {English word: Spanish translation}
    :return: A list of the sentences in spanish
    '''
    f = open("corpus.txt", "r")
    f_write = open("translated_sentences.txt", "w")
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
    '''
    Calculates precision of an ngram model
    :param g_tokens: Google's translations (Reference)
    :param o_tokens: Our translations (Candidate)
    :param n: desired ngram model
    :return: Precision of the ngram model candidate with respect to the reference sentence
    '''
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

def calc_sentence_bleu(g_tokens, o_tokens, f_write):
    '''
    Calculates the BLEU score of a given sentence (given in tokens)
    :param g_tokens: Google's translation of a sentence (Reference)
    :param o_tokens: Our translation of the same sentence (Candidate)
    :param f_write: File to write bleu scores to
    :return: Sentence BLEU Score
    '''
    bleu_num = 0
    blue_denom = 0
    sentence = " ".join(o_tokens)
    sentence = sentence[0].upper() + sentence[1:]
    f_write.write(sentence+"\n")

    for i in range(1,5):
        precision = calc_precision(g_tokens, o_tokens, i)
        if precision != 0:
            bleu_num += precision
            blue_denom += 1
        f_write.write("\t{}-Gram precision of {}\n".format(i, round(precision,5)))

    if (blue_denom != 0):
        bleu = bleu_num/blue_denom
    else:
        bleu = 0

    f_write.write("\n\tTOTAL BLEU Score: {}\n\n".format(round(bleu, 5)))
    return bleu

def bleu_score(translated_sentences):
    '''
    Calculates BLEU scores for the entire translated corpus using sentences in google_translations.txt as references
    Writes scores to bleu_scores.txt
    :param translated_sentences: A list of translated sentences
    :return: None (output in bleu_scores.txt)
    '''
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
    f_write.write("We have a BLEU score of {} on average for the whole system".format(round(blue_avg,5)))
    f.close()
    f_write.close()
    print("BLEU scores for sentences can be seen in bleu_scores.txt")

if __name__ == '__main__':
    # Call grammar construction, translate sentences
    grammar = construct_cfg_from_string()
    parse_original_sentences(grammar)

    english_to_spanish_dict = get_translation_dict()
    translated_sentences = translate_sentences(english_to_spanish_dict)
    bleu_score(translated_sentences)
    