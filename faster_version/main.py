import pyHook, pythoncom
import pyautogui
import pyperclip
from pyHook import HookConstants, GetKeyState
from BanglaPhoneticParser import *
import keyboard
import threading
import tkinter as tk
import time

from Database import database_handler
from faster_version.global_initializer import *
from helper_functions import *
from faster_version.helper_functions import get_clipboard_data
from faster_version.gui import meaning

global suggestions
suggestions = ['suggestions' + str(i) for i in range(10)]


class BackSpace(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        pass

    def run(self):
        time.sleep(.1)
        global do_process_key
        do_process_key = False
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('space')
        do_process_key = True


# load bangla dict
from load_dict_words import load_bangla_to_english_dict

global b2e
b2e = load_bangla_to_english_dict()


def predict_with_lstm(current_sentence):
    result = (model.sample(sess, chars, vocab, 500, current_sentence, 1).encode('utf-8'))
    result = result.decode("utf-8", "replace")
    result = process_bangla(result)
    type(result)

    result = result.split(" ")

    # word = (result.split(" ")[(len(current_sentence.split(" "))) - 1])
    current_sentence_len = current_sentence.split(" ")
    result = result[len(current_sentence_len) - 1:]

    global index_of_suggestion_sentence
    index_of_suggestion_sentence = 0

    global suggest_sentence
    suggest_sentence = result[1:]

    suggestion_1 = ' '.join(suggest_sentence[0: index_of_suggestion_sentence + 1])
    suggestion_2 = ' '.join(suggest_sentence[index_of_suggestion_sentence + 1: 7])

    suggestions[8] = suggestion_1
    suggestions[9] = suggestion_2


def myfunc(item):
    global do_process_key
    do_process_key = False

    del_current_word()

    pyperclip.copy(item)
    pyautogui.hotkey("ctrl", "v")

    do_process_key = True

    print(item)


def del_current_word():
    # print('called delete')
    keyboard.release('ctrl')
    n = len(current_word)
    for i in range(n):
        keyboard.press_and_release('backspace')

    global current_word, current_bangla_word
    current_word = ""
    current_bangla_word = ""


def process_keypress(last_char):
    last_char = str.lower(last_char)
    global current_word, current_bangla_word, current_bangla_sentence, current_sentence, prev_char

    if last_char == 'return':
        if enabled_language == "bangla":
            current_bangla_sentence = BanglaPhoneticParser.parse(current_sentence)
            database_handler.insert_sentence(current_bangla_sentence)
        else:
            database_handler.insert_sentence(current_sentence)

        current_sentence = ""
        current_bangla_sentence = ""
        current_word = ""
        current_bangla_word = ""

    elif last_char == 'back':
        # update current
        if len(current_sentence) > 1:
            if (len(current_word)) > 1:
                current_word = current_word[:-1]
            current_sentence = current_sentence[:-1]
            current_bangla_word = BanglaPhoneticParser.parse(current_word)
        else:
            current_word = ""
            current_sentence = ""
            current_bangla_word = ""

    # Detect end of word
    elif last_char == 'oem_period' or last_char == '?' or last_char == 'space':
        if enabled_language == "bangla":
            current_bangla_sentence = BanglaPhoneticParser.parse(current_sentence)
            current_bangla_word = BanglaPhoneticParser.parse(current_word)

            myfunc(current_bangla_word)

            predict_with_lstm(current_bangla_sentence)
        else:
            predict_with_lstm(current_sentence)
            pass

        current_word = ""
        current_bangla_word = ""
        current_sentence += " "

        # escape other keypress
    elif len(last_char) > 1:
        pass

    else:
        if prev_char == 'lshift' or prev_char == 'rshift':
            if 'a' <= last_char <= 'z':
                last_char = last_char.upper()

        current_sentence += last_char
        current_word += last_char
        if enabled_language == "bangla":
            current_bangla_word = BanglaPhoneticParser.parse(current_word)

    prev_char = last_char

    if enabled_language == "bangla":
        suggestions[0] = current_bangla_word
        # load other five suggestion
        words = bangla_word_search(current_bangla_word[:-1])  # removing one extra space
        # print('"',current_bangla_word,'"', words)
        for i in range(len(words)):
            suggestions[i + 1] = words[i]

    else:
        suggestions[0] = current_word
        # load other five suggestion
        words = english_word_search(current_word)

        for i in range(len(words)):
            suggestions[i + 1] = words[i]


def OnKeyboardEvent(event):
    if not do_process_key:
        return True

    if event.Key == 'Insert':
        global index_of_suggestion_sentence
        index_of_suggestion_sentence += 1

        suggestion_1 = ' '.join(suggest_sentence[0: index_of_suggestion_sentence + 1])
        suggestion_2 = ' '.join(suggest_sentence[index_of_suggestion_sentence + 1: 9])

        suggestions[8] = suggestion_1
        suggestions[9] = suggestion_2

    if '0' <= event.Key <= '9':
        # if GetKeyState(HookConstants.VKeyToID('VK_CONTROL')) and HookConstants.IDToName(event.KeyID) == str(i):
        if prev_char == 'lcontrol':
            print("Ctrl " + event.Key + " pressed")

            global do_process_key
            do_process_key = False

            # del_current_word(current_word)
            # pyperclip.copy(suggestions[i])
            # pyautogui.hotkey("ctrl", "v")

            myfunc(suggestions[int(event.Key)])

            back = BackSpace()
            do_process_key = True

            return True

    if event.Key == 'C':
        # if GetKeyState(HookConstants.VKeyToID('VK_CONTROL')) and HookConstants.IDToName(event.KeyID) == str(i):
        if prev_char == 'lcontrol':
            # print("Ctrl " + event.Key + " pressed")

            english_word = get_clipboard_data()
            if english_word is not None:
                if english_word[-1] == ' ':
                    english_word = english_word[:-1]

                print(english_word)
                if english_word in b2e.keys():
                    bangla_word = b2e[english_word]
                    print("$$Dictionary data", bangla_word)

                    meaning_window = meaning(bangla_word)

    if True:
        # print(event.Key)
        process_keypress(event.Key)

    # debug stuff
    # print("current word: ", current_word)
    # print("current bangla word ", current_bangla_word)
    # print("current sentence ", current_sentence)
    # print("current bangla sentence ", current_bangla_sentence)
    print()

    app.updateGui(suggestions)
    return True


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
