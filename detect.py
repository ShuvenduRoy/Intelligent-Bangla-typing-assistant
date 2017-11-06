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

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError:  # Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font


def create_gui():
    """ Create GUI window to show suggesting"""
    global root
    root = tk.Tk()
    global label
    helv36 = font.Font(family='Helvetica', size=30, weight='bold')
    label = tk.Label(root, font=helv36)

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    root.geometry('+%d+%d' % (50, 50))

    root.overrideredirect(True)
    # root.geometry("+250+250")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    root.attributes("-alpha", 0.7)


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

    text = label.cget("text")
    text += last_char.lower()

    label.config(text=text)

    label.pack()
    root.mainloop()


def show(string):
    """ show the string in gui"""

    if 'root' not in globals():
        create_gui()

    label.config(text=string)

    label.pack()
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
    word = result.split("\n")[0].split(" ")[len(current_sentence.split(" "))-1]

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

    result = (model.sample(sess, chars, vocab, 500, current_sentence, 1).encode('utf-8'))
    # print(result)

    result = result.decode("utf-8", "replace")
    print(result)

    word = (result.split(" ")[(len(current_sentence.split(" "))) - 1])

    # word = result.split("\n")[0].split(" ")[len(current_sentence.split(" ")) - 1]

    if word is not None:
        show(word)


def process_keypress(last_char):
    """Handle user keypress according to settings"""
    last_char = str.lower(last_char)

    # Initialize global variables
    if 'current_sentence' not in globals():
        global current_sentence
        current_sentence = ""

        global current_word
        current_word = ""

        global saved_args, chars, vocab, model, saver, ckpt

        saved_model_path = "save/english"

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
    if last_char == 'Oem_Period' or last_char == 'return' or last_char == '?':
        database_handler.insert_sentence(current_sentence)
        current_sentence = ""
        current_word = ""

    elif last_char == 'back':
        # update current
        current_word = current_word[:-1]
        current_sentence = current_sentence[:-1]

    # Detect end of word
    elif last_char == 'space':
        # update current
        current_word = ""
        current_sentence += " "

        # functionality 1: Direct find sentence from history
        # find_from_history_given_words(current_sentence)

        # functionality 2: use LSTM to suggest next word
        predict_with_lstm(current_sentence)

    # escape other keypress
    elif len(last_char) > 1:
        pass

    else:
        current_sentence += last_char
        current_word += last_char

    # print(current_sentence)
    print("sentence: ", current_sentence)
    # print("word: ", current_word)

    # show the typing
    # show_typing(last_char)


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


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
