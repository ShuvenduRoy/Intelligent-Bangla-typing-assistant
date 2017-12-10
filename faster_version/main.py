import pyHook, pythoncom
import pyautogui
import pyperclip
from pyHook import HookConstants, GetKeyState
from BanglaPhoneticParser import *
import keyboard
import threading
import tkinter as tk

from Database import database_handler
from faster_version.global_initializer import *
from load_dict_words import bangla_word_search, english_word_search

global suggestions
suggestions = ['suggestions' + str(i) for i in range(8)]


def myfunc(item):
    global do_process_key
    do_process_key = False

    del_current_word()

    pyperclip.copy(item)
    pyautogui.hotkey("ctrl", "v")

    do_process_key = True

    print(item)


def del_current_word():
    print('called delete')
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

    if last_char == 'oem_period' or last_char == 'return' or last_char == '?':
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
    elif last_char == 'space':
        if enabled_language == "bangla":
            current_bangla_sentence = BanglaPhoneticParser.parse(current_sentence)
            current_bangla_word = BanglaPhoneticParser.parse(current_word)

            myfunc(current_bangla_word)

            # predict_with_lstm(current_bangla_sentence)
        else:
            # predict_with_lstm(current_sentence)
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

    if '0' <= event.Key <= '7':
        # if GetKeyState(HookConstants.VKeyToID('VK_CONTROL')) and HookConstants.IDToName(event.KeyID) == str(i):
        if prev_char == 'lcontrol':
            print("Ctrl " + event.Key + " pressed")

            global do_process_key
            do_process_key = False

            # del_current_word(current_word)
            # pyperclip.copy(suggestions[i])
            # pyautogui.hotkey("ctrl", "v")

            myfunc(suggestions[int(event.Key)])

            do_process_key = True
            return True

    if True:
        print("prev key", prev_char)
        print(event.Key)
        process_keypress(event.Key)

    # debug stuff
    print("current word: ", current_word)
    print("current bangla word ", current_bangla_word)
    print("current sentence ", current_sentence)
    print("current bangla sentence ", current_bangla_sentence)
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
