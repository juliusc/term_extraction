import spacy
import sys

import argparse

from collections import Counter

def load_unigram_frequency(file):
    frequencies = {}
    for line in open(file):
        word, frequency = line.strip().split()
        frequencies[word] = int(frequency)
    return frequencies


def main(args):
    unigram_frequencies = load_unigram_frequency("unigram_count.txt")

    nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser'])
    token_counts = Counter()
    for line in open(args.text_file):
        doc = nlp(line)
        for token in doc: 
            if token.pos_ in ["NOUN", "PROPN"]:
                token_counts[token.text.lower()] += 1

    scores = {}
    for token, count in token_counts.items():
        if token in unigram_frequencies:
            scores[token] = count / unigram_frequencies[token]

    for token, _ in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"{token}\t{token_counts[token]}\t{unigram_frequencies[token]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a document, print all nouns, their frequencies in the "
                    "document, and their frequencies in a general internet corpus")

    parser.add_argument("text_file", help="Text file")

    args = parser.parse_args()
    main(args)
