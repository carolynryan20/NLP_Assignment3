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

if __name__ == '__main__':
    main()