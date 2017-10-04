# importing packages
import pythoncom, pyHook

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError:  # Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font


def create_gui(last_char):
    if 'root' not in globals():
        global root
        root = tk.Tk()
        global label
        helv36 = font.Font(family='Helvetica', size=30, weight='bold')
        label = tk.Label(root, font=helv36)

        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen

        root.geometry('+%d+%d' % (50, 50))

    text = label.cget("text")
    text += last_char.lower()

    label.config(text=text)

    root.overrideredirect(True)
    # root.geometry("+250+250")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    root.attributes("-alpha", 0.7)
    label.pack()
    root.mainloop()


def process_input(last_char):
    if len(last_char) == 1:
        create_gui(last_char)
    elif last_char == "Space":
        create_gui(" ")


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
    process_input(event.Key)

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
