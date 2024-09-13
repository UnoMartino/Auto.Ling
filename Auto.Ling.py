import tkinter as tk
from tkinter import ttk
import instalingAutomator
import os
from sys import platform


def editAccounts():
    if platform == "win32":
        os.system("notepad ./secrets.txt")
    elif platform == "linux":
        os.system("gedit ./secrets.txt")
    elif platform == "darwin":
        os.system("open -a TextEdit ./secrets.txt")


def main():
    root = tk.Tk()
    root.title("Auto.Ling")
    root.geometry('600x510')
    root.resizable(False, False)
    root.config(background="#434c5e")

    ttk.Label(root, text="Auto.Ling", font="sans-serif 20", background="#434c5e", foreground="#e5e9f0").pack(fill=tk.X, pady=10, padx=10)

    ttk.Label(root, text="Witaj w Auto.Ling! Aby rozpocząć, wpisz swoje dane logowania do Insta.Ling i kliknij przycisk 'Uruchom'.", background="#434c5e", foreground="#e5e9f0").pack(fill=tk.X, pady=(10, 5), padx=10)
    ttk.Label(root, text="Nie klikaj nic w przeglądarce. Skrypt sam zrobi wszystko.", background="#434c5e", foreground="#e5e9f0").pack(fill=tk.X, pady=(0, 10), padx=10)


    username = tk.StringVar()
    password = tk.StringVar()
    doNotReplaceWords = tk.StringVar()
    doNotReplaceWords.set("0")
    allAccounts = tk.StringVar()
    allAccounts.set("1")
    slowInternetModeTk = tk.StringVar()
    slowInternetModeTk.set("0")
    randomWordTime = tk.StringVar()
    randomWordTime.set("0")


    with open("./secrets.txt", "r") as file:
        fileContent = file.readlines()
        try:
            if fileContent[0] != "" or fileContent[0] != ":":
                username.set(fileContent[0].split(":")[0])
                password.set(fileContent[0].split(":")[1])
                if len(fileContent) > 1:
                    allAccounts.set("1")
                else:
                    allAccounts.set("0")
        except:
            pass
    
    with open("./words.json", "r") as file:
        fileContent = file.readlines()
        if fileContent == [] or fileContent == [""]:
            doNotReplaceWords.set("0")
        else:
            doNotReplaceWords.set("1")

    ttk.Label(root, text="Login:", background="#434c5e", foreground="#e5e9f0").pack(anchor=tk.W, padx=10)
    ttk.Entry(root, textvariable=username).pack(fill=tk.X, pady=10, padx=10)
    ttk.Label(root, text="Hasło:", background="#434c5e", foreground="#e5e9f0").pack(anchor=tk.W, padx=10)
    ttk.Entry(root, textvariable=password, show="*").pack(fill=tk.X, pady=10, padx=10)

    ttk.Button(root, text="Edytuj konta", command=editAccounts).pack(fill=tk.X, pady=10, padx=10)


    def login():
        file = open("./secrets.txt", "r")
        secretsFile = file.readlines()
        file.close()
        if username.get() + ":" + password.get() not in secretsFile:
            with open("./secrets.txt", "a") as file:
                file.write(username.get() + ":" + password.get() + "\n")   
        
        instalingAutomator.variables()
        if slowInternetModeTk.get() == "1":
            instalingAutomator.slowInternetMode = True

        if randomWordTime.get() == "1":
            instalingAutomator.randomWordTimeMode = True

        instalingAutomator.getSecrets()
        if allAccounts.get() == "1":
            for i in range(0, len(instalingAutomator.usernames)):
                instalingAutomator.login(i)
                if doNotReplaceWords.get() == "0":
                    instalingAutomator.saveWords()
                instalingAutomator.doSession()
                instalingAutomator.logout()
        elif allAccounts.get() == "0":
            instalingAutomator.login(0)
            if doNotReplaceWords.get() == "0":
                instalingAutomator.saveWords()
            instalingAutomator.doSession()

        instalingAutomator.driver.quit()



    style = ttk.Style()
    style.map("Custom.TCheckbutton", foreground=[('!active', '#e5e9f0'),('pressed', '#e5e9f0'), ('active', '#e5e9f0')], background=[ ('!active','#434c5e'),('pressed', '#434c5e'), ('active', '#434c5e')], font="sans-serif 10")
    ttk.Checkbutton(root, text="Nie pobieraj słówek automatycznie", variable=doNotReplaceWords, style="Custom.TCheckbutton", offvalue="0", onvalue="1").pack(fill=tk.X, pady=10, padx=10)
    ttk.Checkbutton(root, text="Wszystkie konta", variable=allAccounts, style="Custom.TCheckbutton", offvalue="0", onvalue="1").pack(fill=tk.X, pady=10, padx=10)
    ttk.Checkbutton(root, text="Tryb wolnego internetu", variable=slowInternetModeTk, style="Custom.TCheckbutton", offvalue="0", onvalue="1").pack(fill=tk.X, pady=10, padx=10)
    ttk.Checkbutton(root, text="Losuj czas uzupełnienia słówka", variable=randomWordTime, style="Custom.TCheckbutton", offvalue="0", onvalue="1").pack(fill=tk.X, pady=10, padx=10)


    ttk.Button(root, text="Uruchom", command=login).pack(fill=tk.X, pady=10, padx=10)


    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()


if __name__ == "__main__":
    main()