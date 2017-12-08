def load_english_word():
    file = open('data/words.txt')

    global eng_words
    eng_words = []
    for line in file:
        eng_words.append(line)


def english_word_search(start):
    if 'eng_words' not in globals():
        load_english_word()

    words_with_start = []
    for word in eng_words:
        if word.startswith(start):
            words_with_start.append(word[:-1])

            if len(words_with_start) == 5:
                return words_with_start
    return words_with_start


def load_bangla_word():
    import io
    file = io.open("data/Bangla_word.txt", mode="r", encoding="utf-8")

    global bangla_words
    bangla_words = []
    for line in file:
        bangla_words.append(line)


def bangla_word_search(start):
    if 'bangla_words' not in globals():
        load_bangla_word()

    words_with_start = []
    for word in bangla_words:
        if word.startswith(start):
            words_with_start.append(word[:-1])

            if len(words_with_start) == 5:
                return words_with_start
    return words_with_start

if __name__ == '__main__':
    print(english_word_search('kf'))
    print(bangla_word_search('যম'))