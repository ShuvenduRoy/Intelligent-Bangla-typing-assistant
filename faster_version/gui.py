import threading
import tkinter as tk


class meaning(threading.Thread):
    def __init__(self, bangla):
        threading.Thread.__init__(self)
        self.bangla = bangla
        self.start()

    def callback(self):
        pass

    def run(self):
        self.root = tk.Tk()
        self.button = tk.Button(self.root, text=self.bangla)
        self.button.pack()

        self.root.mainloop()

