import pyHook, pythoncom
from pyHook import HookConstants, GetKeyState
import keyboard
import threading
import tkinter as tk

from faster_version.global_initializer import current_word, app, do_process_key

global suggestions
suggestions = ['suggestions' + str(i) for i in range(8)]


def OnKeyboardEvent(event):
    if not do_process_key:
        return True

    print(event.Key)
    for i in range(8):
        if GetKeyState(HookConstants.VKeyToID('VK_CONTROL')) and HookConstants.IDToName(event.KeyID) == str(i):
            print("Ctrl " + str(i) + " pressed")

            global disabled
            disabled = True
            # del_current_word(current_word)

            # for j in range(8):
            #     print('$'+suggestions[j]+'$')

            global suggestions
            # print_on("", suggestions[i] + ' ')
            # print(suggestions[i])

            disabled = False

            # TODO handle ctrl+num
            return True

    if True:
        print(event.Key)

    suggestions[0] = event.Key
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
