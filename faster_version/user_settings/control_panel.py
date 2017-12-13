import tkinter as tk

root = tk.Tk()

v = tk.IntVar()
v.set(0)  # initializing the choice, i.e. Python

languages = ["bangla","english"]
dictionary = ["yes","no"]

def update_file(idx):
    textToupdate=""
    if(idx==0):
        textToupdate=languages[1]
    else:
        textToupdate=languages[0]
    #print(textToupdate)
    #root.destroy()
    with open('global_settings.txt', 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(textToupdate,languages[idx])
    #filedata = filedata.replace('yes', 'no')

    # Write the file out again
    with open('global_settings.txt', 'w') as file:
        file.write(filedata)
def update_file_for_dict(idx):
    textToupdate=""
    if(idx==0):
        textToupdate=dictionary[1]
    else:
        textToupdate=dictionary[0]
    #print(textToupdate)
    root.destroy()
    with open('global_settings.txt', 'r') as file:
        filedata = file.read()
    # Replace the target string
    #filedata = filedata.replace(textToupdate,languages[idx])
    filedata = filedata.replace(textToupdate,dictionary[idx])

    # Write the file out again
    with open('global_settings.txt', 'w') as file:
        file.write(filedata)

def ShowChoice():
    if(v.get()==0):
        #print(languages[v.get()])
        update_file(v.get())
    elif(v.get()==1):
        #print(languages[v.get()])
        update_file(v.get())
    # Read in the file
def ShowChoicefordict():
    if (v.get() == 0):
        # print(languages[v.get()])
        update_file_for_dict(v.get())
        print(dictionary[v.get()])
    elif (v.get() == 1):
        # print(languages[v.get()])
        update_file_for_dict(v.get())
        print(dictionary[v.get()])
        # Read in the file
label1=tk.Label(root,
         text="""Choose your favourite language:""",
         justify = tk.LEFT,
         padx = 20).pack()

for val, language in enumerate(languages):
    tk.Radiobutton(root,
                  text=language,
                  padx = 20,
                  variable=v,
                  command=ShowChoice,
                  value=val).pack(anchor=tk.W)
label2=tk.Label(root,
         text="""Do you want to use the dictionary? """,
         justify = tk.LEFT,
         padx = 20).pack()

for val, dict in enumerate(dictionary):
    tk.Radiobutton(root,
                  text=dict,
                  padx = 20,
                  variable=v,
                  command=ShowChoicefordict,
                  value=val).pack(anchor=tk.W)


root.mainloop()