# importing packages
from __future__ import print_function
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

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError:  # Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font


def updateGui():
    suggest_sentenece_selected.set("1")
    suggest_sentenece_unselected.set("2")
    inputList[0].set("hi hey")
    inputList[1].set("there")


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

    screen_width = int(root.winfo_screenwidth() * .40)
    screen_height = int(root.winfo_screenheight() * .05)
    screen_resolution = '0' + '0' + str(screen_width) + 'x' + str(screen_height)

    root.geometry(screen_resolution)

    # root.geometry("500x90+0+0")
    global inputList
    inputList = [StringVar() for _ in range(6)] # ['option 1', 'option 2', 'option 3', 'option 4', 'option 5', 'option 6']

    global buttonList
    buttonList = [None] * (len(inputList))

    def myfunc(item):
        print(item.get())
        root.destroy()
        del globals()['root']

    global suggest_sentenece_selected
    suggest_sentenece_selected = StringVar()

    global  suggest_sentenece_unselected
    suggest_sentenece_unselected = StringVar()

    fm = Frame(root)
    suggest_sentenece_selected_btn = Button(fm, textvariable=suggest_sentenece_selected,
                                        command=lambda: myfunc(suggest_sentenece_selected), bd=0, activeforeground="blue",
                                        justify=LEFT, height=2, padx=10).pack(side=LEFT)

    suggest_sentenece_unselected_btn = Button(fm, textvariable=suggest_sentenece_unselected,
                                        command=lambda: myfunc(suggest_sentenece_unselected), bd=0, activeforeground="blue",
                                        justify=LEFT, height=2, padx=10).pack(side=LEFT)
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

    buttonList[index].config(text=string)

    # label.pack()
    root.mainloop()


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
    # with tf.Session() as sess:
    #     tf.global_variables_initializer().run()
    #     saver = tf.train.Saver(tf.global_variables())
    #     ckpt = tf.train.get_checkpoint_state("save")
    #     if ckpt and ckpt.model_checkpoint_path:
    #         saver.restore(sess, ckpt.model_checkpoint_path)
    #         result = str((model.sample(sess, chars, vocab, 500, current_sentence, 1).encode('utf-8')))
    #         print(result)
    #
    #         word = result.split("\n")[0].split(" ")[len(current_sentence.split(" ")) - 1]
    #
    #         if word is not None:
    #             show(word)

    # current_sentence = "একটি "

    # Changing model for bangla
    # if enabled_language == "bangla":
    #     current_sentence = BanglaPhoneticParser.parse(current_sentence)

    result = (model.sample(sess, chars, vocab, 500, current_sentence, 1).encode('utf-8'))
    # print(result)

    result = result.decode("utf-8", "replace")
    print(result)

    word = (result.split(" ")[(len(current_sentence.split(" "))) - 1])

    # word = result.split("\n")[0].split(" ")[len(current_sentence.split(" ")) - 1]

    if word is not None:
        show(word, 1)


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
        # update current
        current_word = ""
        current_bangla_word = ""
        current_sentence += " "

        # functionality 1: Direct find sentence from history
        # find_from_history_given_words(current_sentence)

        # functionality 2: use LSTM to suggest next word
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

        # print(prev_char, last_char)

        current_sentence += last_char
        current_word += last_char
        if enabled_language == "bangla":
            current_bangla_word = BanglaPhoneticParser.parse(current_word)

    # print(current_sentence)
    print("current sentence: ", current_sentence, "   ", current_bangla_sentence)
    print("current word    : ", current_word, "   ", current_bangla_word)
    prev_char = last_char
    # print("word: ", current_word)

    # show the typing
    # show_typing(last_char)

    # Convert if it bangla is enabled
    if enabled_language == "bangla":
        show(current_bangla_word)


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
    process_keypress(event.Key)

    # return True to pass the event to other handlers
    return True


if __name__ == '__main__':
    show('hi')
