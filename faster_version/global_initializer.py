import tkinter as tk
import threading
import os
from six.moves import cPickle
import tensorflow as tf
from model import Model

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
        self.root.overrideredirect(True)
        # self.root.lift()
        self.root.wm_attributes("-topmost", True)
        # self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.attributes("-alpha", 0.9)
        #
        # self.root.attributes('-fullscreen', False)
        self.root.resizable(width=False, height=False)
        #
        screen_width = int(self.root.winfo_screenwidth() * 1.0)
        screen_height = 65  # int(self.root.winfo_screenheight() * .06)

        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        self.root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, hs - 105))

        self.root.mainloop()


global app
app = App()

global current_sentence, current_bangla_sentence
current_sentence = ""
current_bangla_sentence = ""

global current_word, current_bangla_word, prev_char
current_word = ""
current_bangla_word = ""
prev_char = ""

# global saved_args, chars, vocab, model, saver, ckpt
#
# # path for models
# global bangla_model_path, english_model_path
# bangla_model_path = "save/bangla"
# english_model_path = "save/english"


# saved_model_path = bangla_model_path if enabled_language == "bangla" else english_model_path
#
# with open(os.path.join(saved_model_path, 'config.pkl'), 'rb') as f:
#     saved_args = cPickle.load(f)
# with open(os.path.join(saved_model_path, 'chars_vocab.pkl'), 'rb') as f:
#     chars, vocab = cPickle.load(f)
#
# model = Model(saved_args, training=False)
#
# global sess
# sess = tf.Session()
# sess.run(tf.global_variables_initializer())
#
# saver = tf.train.Saver(tf.global_variables())
# ckpt = tf.train.get_checkpoint_state(saved_model_path)
# if ckpt and ckpt.model_checkpoint_path:
#     saver.restore(sess, ckpt.model_checkpoint_path)
