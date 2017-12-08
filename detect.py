# importing packages
from __future__ import print_function

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


def updateGui():
    suggest_sentenece_selected.set(suggestions[6])
    suggest_sentenece_unselected.set(suggestions[7])

    for i in range(6):
        inputList[i].set(suggestions[i])

    # inputList[5].set('hi there')


def change_gui_mode():
    global root
    root.destroy()

    root = tk.Tk()
    root.wm_attributes("-topmost", True)
    root.attributes('-fullscreen', False)
    root.resizable(width=False, height=False)

    screen_width = int(root.winfo_screenwidth() * 1.0)
    screen_height = 65  # int(root.winfo_screenheight() * .06)

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, hs - 105))

    root.overrideredirect(True)  # disable title bar<blank>
    # root.lift()
    # root.wm_attributes("-topmost", True)
    # root.wm_attributes("-disabled", True)     # make unclickable
    # root.wm_attributes("-transparentcolor", "white")

    global inputList
    inputList = [StringVar() for _ in range(6)]

    global buttonList
    buttonList = [None] * (len(inputList))

    global suggest_sentenece_selected
    suggest_sentenece_selected = StringVar()

    global suggest_sentenece_unselected
    suggest_sentenece_unselected = StringVar()

    fm = Frame(root)
    suggest_sentenece_selected_btn = Button(fm, textvariable=suggest_sentenece_selected,
                                            command=lambda: myfunc(suggest_sentenece_selected), bd=0,
                                            activeforeground="blue",
                                            justify=LEFT, height=2, padx=10)
    suggest_sentenece_selected_btn.pack(side=LEFT)
    suggest_sentenece_selected_btn.bind("<Return>", lambda x: myfunc(suggest_sentenece_selected))

    suggest_sentenece_unselected_btn = Button(fm, textvariable=suggest_sentenece_unselected,
                                              command=lambda: myfunc(suggest_sentenece_unselected), bd=0,
                                              activeforeground="blue",
                                              justify=LEFT, height=2, padx=10)
    suggest_sentenece_unselected_btn.pack(side=LEFT)
    suggest_sentenece_unselected_btn.bind("<Return>", lambda x: myfunc(suggest_sentenece_unselected))
    fm.pack(side=TOP)

    fm2 = Frame(root)
    buttonList[0] = Button(fm2, textvariable=inputList[0], command=lambda: myfunc(inputList[0]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)

    buttonList[0].pack(side=LEFT)
    buttonList[0].bind("<Return>", lambda x: myfunc(inputList[0]))
    buttonList[1] = Button(fm2, textvariable=inputList[1], command=lambda: myfunc(inputList[1]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[1].pack(side=LEFT)
    buttonList[1].bind("<Return>", lambda x: myfunc(inputList[1]))

    buttonList[2] = Button(fm2, textvariable=inputList[2], command=lambda: myfunc(inputList[2]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[2].pack(side=LEFT)
    buttonList[2].bind("<Return>", lambda x: myfunc(inputList[2]))

    buttonList[3] = Button(fm2, textvariable=inputList[3], command=lambda: myfunc(inputList[3]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[3].pack(side=LEFT)
    buttonList[3].bind("<Return>", lambda x: myfunc(inputList[3]))

    buttonList[4] = Button(fm2, textvariable=inputList[4], command=lambda: myfunc(inputList[4]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[4].pack(side=LEFT)
    buttonList[4].bind("<Return>", lambda x: myfunc(inputList[4]))

    buttonList[5] = Button(fm2, textvariable=inputList[5], command=lambda: myfunc(inputList[5]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[5].pack(side=LEFT)
    buttonList[5].bind("<Return>", lambda x: myfunc(inputList[5]))
    fm2.pack(side=TOP)

    updateGui()
    root.mainloop()


def create_gui():
    """ Create GUI window to show suggesting"""
    # global root
    # root = tk.Tk()
    # global label
    # helv36 = font.Font(family='Helvetica', size=30, weight='bold')
    # label = tk.Label(root, font=helv36)
    #
    # # get screen width and height
    # ws = root.winfo_screenwidth()  # width of the screen
    # hs = root.winfo_screenheight()  # height of the screen
    #
    # root.geometry('+%d+%d' % (50, 50))
    #
    # root.overrideredirect(True)
    # # root.geometry("+250+250")
    # root.lift()
    # root.wm_attributes("-topmost", True)
    # root.wm_attributes("-disabled", True)
    # root.wm_attributes("-transparentcolor", "white")
    # root.attributes("-alpha", 0.7)

    global root
    root = Tk()
    # global label
    # label = tk.Label(root)

    # Zodi button er text ta cas taile buttonList[0]['text'] likhle button er text ta diye dibe

    root.attributes('-fullscreen', False)
    root.resizable(width=False, height=False)

    screen_width = int(root.winfo_screenwidth() * 1.0)
    screen_height = 65  # int(root.winfo_screenheight() * .06)

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, hs - 105))

    global suggestions
    suggestions = []
    for i in range(8):
        suggestions.append("<blank>")

    # suggestions[6] = 'test'

    # root.geometry("500x90+0+0")
    global inputList
    inputList = [StringVar() for _ in range(6)]

    global buttonList
    buttonList = [None] * (len(inputList))

    global suggest_sentenece_selected
    suggest_sentenece_selected = StringVar()

    global suggest_sentenece_unselected
    suggest_sentenece_unselected = StringVar()

    fm = Frame(root)
    suggest_sentenece_selected_btn = Button(fm, textvariable=suggest_sentenece_selected,
                                            command=lambda: myfunc(suggest_sentenece_selected), bd=0,
                                            activeforeground="blue",
                                            justify=LEFT, height=2, padx=10)
    suggest_sentenece_selected_btn.pack(side=LEFT)
    suggest_sentenece_selected_btn.bind("<Return>", lambda x: myfunc(suggest_sentenece_selected))

    suggest_sentenece_unselected_btn = Button(fm, textvariable=suggest_sentenece_unselected,
                                              command=lambda: myfunc(suggest_sentenece_unselected), bd=0,
                                              activeforeground="blue",
                                              justify=LEFT, height=2, padx=10)
    suggest_sentenece_unselected_btn.pack(side=LEFT)
    suggest_sentenece_unselected_btn.bind("<Return>", lambda x: myfunc(suggest_sentenece_unselected))
    fm.pack(side=TOP)

    fm2 = Frame(root)
    buttonList[0] = Button(fm2, textvariable=inputList[0], command=lambda: myfunc(inputList[0]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)

    buttonList[0].pack(side=LEFT)
    buttonList[0].bind("<Return>", lambda x: myfunc(inputList[0]))
    buttonList[1] = Button(fm2, textvariable=inputList[1], command=lambda: myfunc(inputList[1]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[1].pack(side=LEFT)
    buttonList[1].bind("<Return>", lambda x: myfunc(inputList[1]))

    buttonList[2] = Button(fm2, textvariable=inputList[2], command=lambda: myfunc(inputList[2]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[2].pack(side=LEFT)
    buttonList[2].bind("<Return>", lambda x: myfunc(inputList[2]))

    buttonList[3] = Button(fm2, textvariable=inputList[3], command=lambda: myfunc(inputList[3]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[3].pack(side=LEFT)
    buttonList[3].bind("<Return>", lambda x: myfunc(inputList[3]))

    buttonList[4] = Button(fm2, textvariable=inputList[4], command=lambda: myfunc(inputList[4]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[4].pack(side=LEFT)
    buttonList[4].bind("<Return>", lambda x: myfunc(inputList[4]))

    buttonList[5] = Button(fm2, textvariable=inputList[5], command=lambda: myfunc(inputList[5]), bd=0,
                           activeforeground="blue",
                           justify=LEFT, width=10, height=2, padx=10)
    buttonList[5].pack(side=LEFT)
    buttonList[5].bind("<Return>", lambda x: myfunc(inputList[5]))
    fm2.pack(side=TOP)

    root.overrideredirect(True)
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    root.attributes("-alpha", 0.9)
    # change_gui_mode()
    updateGui()


def show_typing(last_char):
    """append the input right after what was typed before"""
    if 'root' not in globals():
        create_gui()

    # Show any character
    if len(last_char) == 1:
        last_char = last_char

    # Set 'Space' = ' '
    elif last_char == "space":
        last_char = " "

    # Do nothing for other long input like 'Shitf', 'Ctrl'
    else:
        return

    text = buttonList[0].cget("text")
    text += last_char.lower()

    buttonList[0].config(text=text)

    buttonList[0].pack()
    root.mainloop()


def show(string, index=0):
    """ show the string in gui"""

    if 'root' not in globals():
        create_gui()

    # inputList[index].set(string)
    suggestions[index] = string
    updateGui()

    # label.pack()
    root.mainloop()


def suggestion_action_handeler(last_char):
    if last_char == 'Insert':
        global index_of_suggestion_sentence
        index_of_suggestion_sentence += 1

        suggestion_1 = ' '.join(suggest_sentence[0: index_of_suggestion_sentence + 1])
        suggestion_2 = ' '.join(suggest_sentence[index_of_suggestion_sentence + 1: 7])

        suggestions[6] = suggestion_1
        suggestions[7] = suggestion_2

        updateGui()

    elif '0' <= last_char <= '7':
        global disabled
        disabled = True
        index = int(last_char)
        global current_word

        print(current_word)
        print_on("", suggestions[index] + '  ')

        disabled = False


def find_from_history_given_words(current_sentence):
    # get from database
    word = database_handler.string_strart_with(current_sentence)

    # update current
    current_word = ""
    current_sentence += " "

    # show it
    if word is not None:
        show(word[0])


def predict_with_lstm_in_shell(current_sentence):
    result = os.popen('python sample.py --save_dir save --prime "' + current_sentence + '"').read()
    word = result.split("\n")[0].split(" ")[len(current_sentence.split(" ")) - 1]

    if word is not None:
        show(word)


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

    suggestions[6] = suggestion_1
    suggestions[7] = suggestion_2


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
        enabled_language = "english"

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

    # detect end of sentence
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

    if 'root' not in globals():
        create_gui()

    global suggestions
    if enabled_language == "bangla":
        # load other five suggestion
        words = bangla_word_search(current_bangla_word[:-1])  # removing one extra space
        # print('"',current_bangla_word,'"', words)
        for i in range(len(words)):
            suggestions[i + 1] = words[i]

        show(current_bangla_word)
    else:
        # load other five suggestion
        words = english_word_search(current_word)

        for i in range(len(words)):
            suggestions[i + 1] = words[i]

        show(current_word)


def OnKeyboardEvent(event):
    # print('MessageName:',event.MessageName)
    # print('Message:',event.Message)
    # print('Time:',event.Time)
    # print('Window:',event.Window)
    # print('WindowName:',event.WindowName)
    # print('Ascii:', event.Ascii, chr(event.Ascii))
    # print('Key:', event.Key)
    # print('KeyID:', event.KeyID)
    # print('ScanCode:', event.ScanCode)
    # print('Extended:', event.Extended)
    # print('Injected:', event.Injected)
    # print('Alt', event.Alt)
    # print('Transition', event.Transition)
    # print('---')
    # if 'root' in globals():
    #     change_gui_mode()
    if 'disabled' not in globals():
        global disabled
        disabled = False

    if disabled:
        return True

    if 'do_process_key' not in globals():
        global do_process_key
        do_process_key = True

    if event.Key == 'Retuen':
        do_process_key = True



    if do_process_key:
        process_keypress(event.Key)
    else:
        suggestion_action_handeler(event.Key)

    # return True to pass the event to other handlers
    return True


def myfunc(item):
    root.destroy()
    del globals()['root']

    global do_process_key
    do_process_key = False

    keyboard.write(item.get())

    # re-enable key processing
    do_process_key = True


def print_on(del_word, item):
    root.destroy()
    del globals()['root']

    global do_process_key
    do_process_key = False

    for i in range(len(del_word)):
        keyboard.press_and_release('backspace')
    keyboard.write(item)
    keyboard.press_and_release('backspace')

    # re-enable key processing
    do_process_key = True


if __name__ == '__main__':
    show('hi')
