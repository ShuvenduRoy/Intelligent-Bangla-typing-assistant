import pyHook, pythoncom
from pyHook import HookConstants, GetKeyState
from global_initializer import *
import keyboard
import threading
import tkinter as tk

from faster_version.global_initializer import current_word


def OnKeyboardEvent(event):
    print('Key:', event.Key)
    # global current_word
    print("current_word: ", current_word)

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

    return True




# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
