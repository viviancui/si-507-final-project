import nltk
from nltk.corpus import stopwords
import json

# FNAME = "lyrics_ironmaiden.py"
# f = open(FNAME, "r")
# lyrics = f.read()
# f.close()
def clear_lyrics(lyrics_str):
    lyrics_str_clear = lyrics_str.replace("...", " ")
    lyrics_str_clear = lyrics_str_clear.replace("******* This Lyrics is NOT for Commercial use *******", " ")
    lyrics_str_clear = lyrics_str_clear.replace("(1409617541815)", " ")
    return lyrics_str_clear
    # print(type(lyrics))
def tokenize(lyrics):
    tokens = nltk.word_tokenize(lyrics)
    tokens_list = []
    for ele in tokens:
        tokens_list.append(ele.lower())
    return tokens_list

# lyrics.most_common()
# print(tokens)

def refine_word(word):
    stop_words_list = set(stopwords.words('english'))
    punctuation = ["-", "@", "na", "gon", "ai", "'n", "ya", "la", "u", "''", "''", "ca", "'d", "``",":", ",", ".", "/", "?", "!", "'", '"', '\"', "\"", "\”", "”", "“", "‘", "’", "#", "(", ")", "'s", "&", ";", ":", "amp", "[", "]", "https", "RT", "http", "HTTPS", "HTTP", "rt", "Rt", "n't", "'re", "'m", "'ll", "'ve"]
    if ((word not in stop_words_list) and (word not in punctuation) and (word is not None)):
        return word
    else:
        return 999
