import tkinter as tk
import threading
import os

import pyautogui
import pyperclip
import keyboard
from six.moves import cPickle
import tensorflow as tf
from model import Model
from tkinter import *

# initialize with one language
global enabled_language
enabled_language = "bangla"


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.inputList = ["position " + str(i) for i in range(8)]
        self.buttonList = [None] * (len(self.inputList))

        self.root.overrideredirect(True)
        # self.root.lift()
        self.root.wm_attributes("-topmost", True)
        # self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.attributes("-alpha", 0.8)
        #
        # self.root.attributes('-fullscreen', False)
        self.root.resizable(width=False, height=False)
        #
        screen_width = int(self.root.winfo_screenwidth() * 1.0)
        screen_height = 65  # int(self.root.winfo_screenheight() * .06)

        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        self.root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, hs - 105))

        fm = Frame(self.root)
        self.buttonList[6] = Button(fm, text=self.inputList[6],
                                    command=lambda: myfunc(self.inputList[6]), bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, height=2, padx=10)
        self.buttonList[6].pack(side=LEFT)
        self.buttonList[6].bind("<Return>", lambda x: myfunc(self.inputList[6]))

        self.buttonList[7] = Button(fm, text=self.inputList[7],
                                    command=lambda: myfunc(self.inputList[7]), bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, height=2, padx=10)
        self.buttonList[7].pack(side=LEFT)
        self.buttonList[7].bind("<Return>", lambda x: myfunc(self.inputList[7]))
        fm.pack(side=TOP)

        fm2 = Frame(self.root)
        self.buttonList[0] = Button(fm2, text=self.inputList[0], command=lambda: myfunc(self.inputList[0]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[0].pack(side=LEFT)
        self.buttonList[0].bind("<Return>", lambda x: myfunc(self.inputList[0]))

        self.buttonList[1] = Button(fm2, text=self.inputList[1], command=lambda: myfunc(self.inputList[1]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[1].pack(side=LEFT)
        self.buttonList[1].bind("<Return>", lambda x: myfunc(self.inputList[1]))

        self.buttonList[2] = Button(fm2, text=self.inputList[2], command=lambda: myfunc(self.inputList[2]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[2].pack(side=LEFT)
        self.buttonList[2].bind("<Return>", lambda x: myfunc(self.inputList[2]))

        self.buttonList[3] = Button(fm2, text=self.inputList[3], command=lambda: myfunc(self.inputList[3]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[3].pack(side=LEFT)
        self.buttonList[3].bind("<Return>", lambda x: myfunc(self.inputList[3]))

        self.buttonList[4] = Button(fm2, text=self.inputList[4], command=lambda: myfunc(self.inputList[4]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[4].pack(side=LEFT)
        self.buttonList[4].bind("<Return>", lambda x: myfunc(self.inputList[4]))

        self.buttonList[5] = Button(fm2, text=self.inputList[4], command=lambda: myfunc(self.inputList[5]),
                                    bd=0,
                                    activeforeground="blue",
                                    justify=LEFT, width=10, height=2, padx=10)
        self.buttonList[5].pack(side=LEFT)
        self.buttonList[5].bind("<Return>", lambda x: myfunc(self.inputList[5]))
        fm2.pack(side=TOP)

        self.root.mainloop()

    def updateGui(self, s):
        for i in range(len(s)):
            self.buttonList[i].config(text=s[i])
            self.inputList[i] = s[i]


global app
app = App()

global current_sentence, current_bangla_sentence
current_sentence = ""
current_bangla_sentence = ""

global current_word, current_bangla_word, prev_char
current_word = ""
current_bangla_word = ""
prev_char = ""

global do_process_key
do_process_key = True


def process_bangla(s):
    import re
    # s = "Example       aaaaaaaaa      \n \r String"
    replaced = re.sub(r'[\n|\r]', ' ', s)
    replaced = re.sub(r' +', ' ', replaced)

    return replaced


def myfunc(item):
    del_current_word(current_word)

    global do_process_key
    do_process_key = False

    pyperclip.copy(item)
    pyautogui.hotkey("ctrl", "v")

    do_process_key = True

    print(item)


def del_current_word(current_word):
    global do_process_key
    do_process_key = False

    n = len(current_word)
    for i in range(n):
        keyboard.press_and_release('backspace')
    do_process_key = True


global saved_args, chars, vocab, model, saver, ckpt

# path for models
global bangla_model_path, english_model_path
bangla_model_path = "save/bangla_wiki"
english_model_path = "save/english"

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
