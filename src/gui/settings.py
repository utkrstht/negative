from tooltip import ToolTip
import tkinter as tk

class Settings:
    def __init__(self, master):
        root = tk.Toplevel(master)
        self.root = root
        root.title("Settings")
        root.geometry("300x300")

        self.username_input_var = tk.StringVar()
        self.show_logs_var = tk.IntVar()

        self.b_deleteall = tk.Button(root, text="Delete all", command=self.on_b_deleteall, fg="#fd2000", bg="#393939", font=("Helvetica", 10, "bold italic"))
        self.b_deleteall.place(x=20, y=250, width=96, height=32)
        ToolTip(self.b_deleteall, "Delete Minecraft and Negative")

        self.b_delete_negative = tk.Button(root, text="Delete Negative", command=self.on_b_delete_negative, fg="#fd2000", bg="#393939", font=("Helvetica", 10, "bold italic"))
        self.b_delete_negative.place(x=20, y=210, width=130, height=30)

        self.b_delete_mc = tk.Button(root, text="Delete Minecraft", command=self.on_b_delete_mc, fg="#fd2000", bg="#393939", font=("Helvetica", 10, "bold italic"))
        self.b_delete_mc.place(x=20, y=170, width=140, height=30)

        self.b_open_logs = tk.Button(root, text="Open Logs", command=self.on_b_open_logs, font=("Helvetica", 10, "italic"))
        self.b_open_logs.place(x=200, y=250, width=80, height=40)

        self.b_open_game = tk.Button(root, text="Open Game Files", command=self.on_b_open_game, font=("Helvetica", 10, "italic"))
        self.b_open_game.place(x=200, y=200, width=80, height=40)

        self.username_input = tk.Entry(root, textvariable=self.username_input_var)
        self.username_input.place(x=20, y=40, width=150, height=28)

        self.username_input_label = tk.Label(root, text="Username (3-16 chars)", font=("Helvetica", 10, "italic"))
        self.username_input_label.place(x=10, y=20, width=160, height=20)

        self.show_logs = tk.Checkbutton(root, text="Show logs during play", variable=self.show_logs_var, font=("Helvetica", 10, "italic"))
        self.show_logs.place(x=20, y=135, width=280, height=30)

        self.negative_size = tk.Label(root, text="Negative Size:", wraplength=90, font=("Helvetica", 10, "italic"))
        self.negative_size.place(x=200, y=10, width=90, height=20)

        self.minecraft_size = tk.Label(root, text="Minecraft Size: ", wraplength=90, font=("Helvetica", 10, "italic"))
        self.minecraft_size.place(x=200, y=70, width=90, height=20)
        ToolTip(self.minecraft_size, "Total Minecraft Size for all installed versions")

        self.l_minecraft_size = tk.Label(root, text="100 MB")
        self.l_minecraft_size.place(x=200, y=90, width=90, height=20)

        self.l_negative_size = tk.Label(root, text="20 MB")
        self.l_negative_size.place(x=195, y=30, width=90, height=20)

    def on_b_deleteall(self):
        pass

    def on_b_delete_negative(self):
        pass

    def on_b_delete_mc(self):
        pass

    def on_b_open_logs(self):
        pass

    def on_b_open_game(self):
        pass

