import tkinter as tk

class Play:
    def __init__(self, master):
        root = tk.Toplevel(master)
        self.root = root
        root.title("Play")
        root.geometry("520x380")

        self.minecraft_version_input_var = tk.StringVar()

        self.minecraft_version = tk.Label(root, text="Minecraft Version", font=("Helvetica", 18, "italic"))
        self.minecraft_version.place(x=10, y=20, width=500, height=40)

        self.minecraft_version_input = tk.Entry(root, textvariable=self.minecraft_version_input_var)
        self.minecraft_version_input.place(x=130, y=60, width=260, height=30)

        self.minecraft_version_input_placeholder = tk.Label(root, text="26.3", font=("Helvetica", 12), state="disabled")
        self.minecraft_version_input_placeholder.place(x=100, y=60, width=100, height=30)

        self.logs = tk.Text(root)
        self.logs.place(x=20, y=230, width=480, height=130)

        self.l_logs = tk.Label(root, text="Logs", font=("Helvetica", 14))
        self.l_logs.place(x=205, y=200, width=110, height=30)

        self.b_launch = tk.Button(root, text="Launch", command=self.on_b_launch, fg="#000000", bg="#bebebe", font=("Helvetica", 12, "italic"))
        self.b_launch.place(x=160, y=140, width=200, height=40)

    def on_b_launch(self):
        pass
