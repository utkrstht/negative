import tkinter as tk

class Credits:
    def __init__(self, master):
        root = tk.Toplevel(master)
        self.root = root
        root.title("Credits")
        root.geometry("250x350")

        self.credits_title = tk.Label(root, text="Credits", font=("Helvetica", 20, "italic"))
        self.credits_title.place(x=20, y=20, width=210, height=40)

        self.credits_developer = tk.Label(root, text="utkrstht - Developer", font=("Helvetica", 11, "bold"))
        self.credits_developer.place(x=35, y=90, width=180, height=30)

        self.credits_gui = tk.Label(root, text="visualtkinter.com - GUI", font=("Helvetica", 11, "bold"))
        self.credits_gui.place(x=35, y=120, width=180, height=30)

        self.label4 = tk.Label(root, text="")
        self.label4.place(x=90, y=260, width=90, height=26)

        self.license = tk.Label(root, text="Licensed under GPLv3", font=("Helvetica", 10, "italic"))
        self.license.place(x=30, y=290, width=180, height=30)

        self.thanks_idea = tk.Label(root, text="aaa - idea")
        self.thanks_idea.place(x=80, y=203, width=90, height=26)

        self.thanks_tester = tk.Label(root, text="technoris - MacOS tester", wraplength=150)
        self.thanks_tester.place(x=60, y=219, width=150, height=30)

        self.thing = tk.Label(root, text="thanks for using", wraplength=100)
        self.thing.place(x=75, y=260, width=100, height=30)

        self.thanks_title = tk.Label(root, text="Thanks", font=("Helvetica", 15, "italic"))
        self.thanks_title.place(x=10, y=163, width=220, height=50)

        self.source = tk.Label(root, text="https://github.com/utkrstht/negative", font=("Helvetica", 9, "italic"))
        self.source.place(x=15, y=305, width=220, height=30)