from tkinter import *
from tkinter import filedialog
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

root = Tk()
root.title("Fuzzy Find Passwords")

resultString = StringVar()
resultString2 = StringVar()
resultString3 = StringVar()
fileDetectedString = StringVar()
pwList = []
searchType = IntVar()
showPasswordBool = False

def openFile():
    global pwList
    pwList.clear()

    try:
        ReadOngoing()
        with open(filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*"))), mode='r', encoding="utf-8", errors='ignore') as pwFile:
            for line in pwFile:
                line = line.strip()
                pwList.append(line)
            ReadSuccess()
    except IOError:
        ReadFailure()
        
def ReadSuccess():
    fileDetectedString.set("File Detected")
    fileDetectedLabel.config(fg="green")

def ReadOngoing():
    fileDetectedString.set('Opening Selected File')
    fileDetectedLabel.config(fg="blue")

def ReadFailure():
    fileDetectedString.set("File Not Found")
    fileDetectedLabel.config(fg="red")

def ResultSearching():
    resultString.set('Searching')
    resultLabel.config(fg="blue")

def ResultIn():
    resultString.set('Results Are In:')
    resultLabel.config(fg="black")

def doComparison(event=None):
    entry1 = inputEntry.get().lower()
    counter = 0
    exactMatch = False

    ResultSearching()
    resultString2.set("")
    resultString3.set("")
    root.update()

    if searchType.get() == 2:
        for password in pwList:
            if fuzz.ratio(entry1, password.lower()) > 84:
                if entry1 == password:
                    exactMatch = True
                else:
                    counter += 1
    else:
        for password in pwList:
            if entry1 == password.lower():
                exactMatch = True
    
    if exactMatch:
        resultString2.set("Exact Match Detected")
    resultString3.set("Number of Similar Matches: %d" % counter)
    ResultIn()

def togglePasswordVisibility():
    global showPasswordBool
    if showPasswordBool:
        inputEntry.config(show="*")
        showPasswordBool = False
    else:
        inputEntry.config(show="")
        showPasswordBool = True

inputEntry = Entry(root, show="*", width=40)
inputEntry.grid(row=0)
inputEntry.bind('<Return>', doComparison)
inputEntry.focus_set()

inputButton = Button(root, text="Search", command = doComparison)
inputButton.grid(row=0, column=1)

searchRadio1 = Radiobutton(root, text="Exact Match Only (Fast)", variable=searchType, value=1)
searchRadio1.grid(row=0, column=2)
searchRadio1.select()
searchRadio2 = Radiobutton(root, text="Find Similar Matches (Slow)", variable=searchType, value=2)
searchRadio2.grid(row=1, column=2)

showPasswordButton = Button(root, text="Show/Hide Password", command=togglePasswordVisibility)
showPasswordButton.grid(row=1, columnspan=2)

fileDetectedLabel = Label(root, textvariable=fileDetectedString)
fileDetectedLabel.grid(row=2, columnspan=2)

findFileBtn = Button(root, text="Open rockyou.txt", command = openFile)
findFileBtn.grid(row=3, columnspan=2)

resultLabel = Label(root, textvariable=resultString)
resultLabel.grid(row=4, columnspan=2)
resultLabel2 = Label(root, textvariable=resultString2, fg="red")
resultLabel2.grid(row=5, columnspan=2)
resultLabel3 = Label(root, textvariable=resultString3, fg="orange")
resultLabel3.grid(row=6, columnspan=2)

mainloop()