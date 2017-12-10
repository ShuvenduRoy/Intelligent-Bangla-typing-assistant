import tkinter as tk
import os
from six.moves import cPickle
import tensorflow as tf
from model import Model

# initialize with one language
global enabled_language
enabled_language = "bangla"

global root
root = tk.Tk()
root.overrideredirect(True)
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
root.attributes("-alpha", 0.9)

root.attributes('-fullscreen', False)
root.resizable(width=False, height=False)

screen_width = int(root.winfo_screenwidth() * 1.0)
screen_height = 65  # int(root.winfo_screenheight() * .06)

ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 0, hs - 105))

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
