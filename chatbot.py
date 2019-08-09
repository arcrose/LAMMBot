import random
import pickle

PICKLE_FILE = "lammdict.dat"

def store_hash(d):
    pickle.dump(d, open(PICKLE_FILE, "w"), -1)

def load_hash():
    try: f = open(PICKLE_FILE, "r")
    except IOError:
        print "Cannot load from " + PICKLE_FILE
        return None
    d = pickle.load(f)
    f.close()
    return d

def hash_input(sentence):
    """Take one sentence and store it into a dictionary."""
    d = {}
    words = sentence.split()
    for i in range(len(words)-2):
        joined = " ".join(words[i:i+2])
        if joined in d:
            d[joined].append([words[i+2]])
        else:
            d[joined] = [words[i+2]]
    return d

def hash_file(filename):
    """Parse a plaintext file containing nothing but straight sentences."""
    try: f = open(filename, "r")
    except IOError:
        print "Cannot open {0}".format(filename)
        return None
    dictionary = {}
    for line in f:
        for sentence in line.lower().split("."):
            d = hash_input(sentence)
            for key in d.keys():
                if key in dictionary:
                    dictionary[key].extend(d[key])
                else:
                    dictionary[key] = d[key]
    f.close()
    return dictionary

def build_sentence(startphrase, d):
    """Build a response starting with startphrase using d."""
    if startphrase not in d:
        return None
    words = startphrase.split()
    sentence = " ".join(words)
    last_two = sentence
    while last_two in d:
        choice = random.choice(d[last_two])
        choice = (choice[0] if isinstance(choice, list) else choice)
        words.append(choice)
        sentence += " " + choice
        last_two = " ".join(words[-2:])
    return sentence

def count_big_words(sentence):
    """Count the number of 'big words' in the sentence."""
    return sum(map(lambda w: 1 if len(w) >= 5 else 0, sentence.split()))

def reply(sentence, d):
    """Form a reply starting from a random part of the input sentence."""
    words = sentence.split()
    if len(words) <= 2:
        return None
    start = random.randrange(0, len(words) - 2)
    return build_sentence(" ".join([words[start], words[start + 1]]) , d)
