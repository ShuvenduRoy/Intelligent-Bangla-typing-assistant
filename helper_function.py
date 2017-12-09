import pyautogui, keyboard


def del_current_word(current_word):
    global disabled, do_process_key
    disabled = True
    do_process_key = False

    n = len(current_word)
    for i in range(n):
        # pyautogui.typewrite(['backspace'])
        keyboard.press_and_release('backspace') # asdfasdfas df


if __name__ == '__main__':
    del_current_word('hi')

