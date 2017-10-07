# importing packages
import pythoncom, pyHook
from Database import database_handler

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError:  # Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font


def create_variables():
    """Create all the variables needed"""

    # store current word, break with 'Space'
    global current_word
    current_word = ""

    # Store current sentence, break with 'Return' or '.'
    global current_sentence
    current_sentence = ""


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
        create_variables()

    # Show any character
    if len(last_char) == 1:
        last_char = last_char

    # Set 'Space' = ' '
    elif last_char == "Space":
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
        create_variables()

    label.config(text = string)

    label.pack()
    root.mainloop()


def process_keypress(last_char):
    """Handle user keypress according to settings"""

    # show the typing
    show_typing(last_char)


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
