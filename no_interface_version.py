from detect import *
# importing packages

import pyautogui
import tensorflow as tf

import argparse
import os
from six.moves import cPickle
from model import Model
from six import text_type
import pythoncom, pyHook
import os
from Database import database_handler
from BanglaPhoneticParser import *
from tkinter import *
import keyboard
import load_dict_words
from load_dict_words import english_word_search, bangla_word_search
from process_text import process_bangla

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError:  # Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font


def print_on(del_word, item):
    global do_process_key
    do_process_key = False

    for i in range(len(del_word)):
        keyboard.press_and_release('backspace')
    keyboard.write(item)
    keyboard.press_and_release('backspace')

    # re-enable key processing
    do_process_key = True


def predict_with_lstm(current_sentence):
    result = (model.sample(sess, chars, vocab, 500, current_sentence, 1).encode('utf-8'))
    result = result.decode("utf-8", "replace")
    result = process_bangla(result)

    word = (result.split(" ")[(len(current_sentence.split(" "))) - 1])

    global index_of_suggestion_sentence
    index_of_suggestion_sentence = 0

    global suggest_sentence
    suggest_sentence = result.split(" ")[1:]

    suggestion_1 = ' '.join(suggest_sentence[0: index_of_suggestion_sentence + 1])
    suggestion_2 = ' '.join(suggest_sentence[index_of_suggestion_sentence + 1: 7])

    print(suggestion_1)
    print(suggestion_2)

    # suggestions[6] = suggestion_1
    # suggestions[7] = suggestion_2


def process_keypress(last_char):
    """Handle user keypress according to settings"""
    last_char = str.lower(last_char)

    # Initialize global variables
    if 'current_sentence' not in globals():
        global current_sentence, current_bangla_sentence
        current_sentence = ""
        current_bangla_sentence = ""

        global current_word, current_bangla_word, prev_char
        current_word = ""
        current_bangla_word = ""
        prev_char = ""

        global saved_args, chars, vocab, model, saver, ckpt

        # path for models
        global enabled_language, bangla_model_path, english_model_path
        bangla_model_path = "save/bangla"
        english_model_path = "save/english"

        # initialize with one language
        global enabled_language
        enabled_language = "bangla"

        saved_model_path = bangla_model_path if enabled_language == "bangla" else english_model_path

        with open(os.path.join(saved_model_path, 'config.pkl'), 'rb') as f:
            saved_args = cPickle.load(f)
        with open(os.path.join(saved_model_path, 'chars_vocab.pkl'), 'rb') as f:
            chars, vocab = cPickle.load(f)

        model = Model(saved_args, training=False)

        global sess
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(saved_model_path)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

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

    elif last_char == 'insert':
        global do_process_key
        do_process_key = False
        change_gui_mode()

    elif last_char == 'back':
        # update current
        if len(current_word) > 1:
            current_word = current_word[:-1]
            current_sentence = current_sentence[:-1]
            current_bangla_word = BanglaPhoneticParser.parse(current_word)
            print(current_bangla_word)
        else:
            current_word = ""
            current_sentence = ""
            current_bangla_word = ""

    # Detect end of word
    elif last_char == 'space':
        if enabled_language == "bangla":
            print('bangla detected')
            print_on(current_word, current_bangla_word)

            for i in range(len(current_word)):
                pyautogui.typewrite(['back'])

        # update current
        current_word = ""
        current_bangla_word = ""
        current_sentence += " "

        if enabled_language == "bangla":
            current_bangla_sentence = BanglaPhoneticParser.parse(current_sentence)
            predict_with_lstm(current_bangla_sentence)
        else:
            predict_with_lstm(current_sentence)

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
    #
    # if 'root' not in globals():
    #     create_gui()

    # global suggestions
    if enabled_language == "bangla":
        words = bangla_word_search(current_bangla_word[:-1])
        print(words)
        # for i in range(len(words)):
        #     suggestions[i + 1] = words[i]

        print('current_bangla_word : ' + current_bangla_word)
        # show(current_bangla_word)
    else:
        words = english_word_search(current_word)
        print(words)
        # for i in range(len(words)):
        # suggestions[i + 1] = words[i]

        print('current_word : ', current_word)
        # show(current_word)
    print()
    print()
    print()


def OnKeyboardEvent(event):
    # print('MessageName:', event.MessageName)
    # print('Message:', event.Message)
    # print('Time:', event.Time)
    # print('Window:', event.Window)
    # print('WindowName:', event.WindowName)
    # print('Ascii:', event.Ascii, chr(event.Ascii))
    # print('Key:', event.Key)
    # print('KeyID:', event.KeyID)
    # print('ScanCode:', event.ScanCode)
    # print('Extended:', event.Extended)
    # print('Injected:', event.Injected)
    # print('Alt', event.Alt)
    # print('Transition', event.Transition)
    # print('---')

    if 'do_process_key' not in globals():
        global do_process_key
        do_process_key = True

    if event.Key == 'Retuen':
        do_process_key = True

    if do_process_key:
        process_keypress(event.Key)

    return True


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
