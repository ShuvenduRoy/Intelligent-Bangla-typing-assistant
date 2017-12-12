import threading
import pyscreenshot as ImageGrab
import re

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


def def_image_data():
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    words = pytesseract.image_to_string(Image.open('im.png'))

    replaced = re.sub('\n|\r|\t', ' ', words)

    newWord = ""
    for i in replaced:
        if ('a' <= i <= 'z') or (i >= 'A' and i <= 'Z'):
            newWord += i
        else:
            newWord += ' '

    newWord = newWord.lower()
    replaced = re.sub(' +', ' ', newWord)
    replaced = re.split(' +', replaced)

    words = []
    for word in replaced:
        if len(word) > 1:
            words.append(word)

    # user_words.extend(words)
    return words


class Screen_analyser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        pass

    def run(self):
        import time
        time.sleep(1)

        if 'user_words' not in globals():
            global user_words
            user_words = []

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
        words = pytesseract.image_to_string(Image.open('im.png'))

        replaced = re.sub('\n|\r|\t', ' ', words)

        newWord = ""
        for i in replaced:
            if (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z'):
                newWord += i
            else:
                newWord += ' '

        newWord = newWord.lower()
        replaced = re.sub(' +', ' ', newWord)
        replaced = re.split(' +', replaced)

        words = []
        for word in replaced:
            if len(word) > 1:
                words.append(word)

        user_words.extend(words)
        print(words)


if __name__ == '__main__':
    im = ImageGrab.grab()
    ImageGrab.grab_to_file('im.png')

    # sa = Screen_analyser()
