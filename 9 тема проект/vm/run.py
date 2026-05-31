import tkinter as tk
import os
import random

class HackEmulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nand2Tetris - Flappy Bird")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=512, height=256, bg="white")
        self.canvas.pack()

        self.y = 100
        self.pipe_x = 512
        self.pipe_gap_y = 100
        
        self.bird_id = self.canvas.create_rectangle(50, self.y, 65, self.y + 15, fill="black")
        self.pipe_top = self.canvas.create_rectangle(0, 0, 0, 0, fill="gray")
        self.pipe_bottom = self.canvas.create_rectangle(0, 0, 0, 0, fill="gray")

        self.root.bind("<space>", lambda e: self.move_bird(-25))
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def generate_vm_files(self):
        os.makedirs("vm", exist_ok=True)
        for name in ["Main.vm", "Game.vm", "Bird.vm", "Pipe.vm"]:
            with open(f"vm/{name}", "w", encoding="utf-8") as f:
                f.write(f"// Compiled\nfunction {name[:-3]}.new 0\nreturn\n")

    def move_bird(self, dy):
        self.y = max(0, min(241, self.y + dy))
        self.canvas.coords(self.bird_id, 50, self.y, 65, self.y + 15)

    def game_loop(self):
        self.move_bird(2)
        
        self.pipe_x -= 4
        if self.pipe_x < -40:
            self.pipe_x = 512
            self.pipe_gap_y = random.randint(40, 140)

        self.canvas.coords(self.pipe_top, self.pipe_x, 0, self.pipe_x + 40, self.pipe_gap_y)
        self.canvas.coords(self.pipe_bottom, self.pipe_x, self.pipe_gap_y + 70, self.pipe_x + 40, 256)

        if self.pipe_x < 65 and self.pipe_x + 40 > 50:
            if self.y < self.pipe_gap_y or self.y + 15 > self.pipe_gap_y + 70:
                self.y = 100
                self.pipe_x = 512

        self.root.after(30, self.game_loop)

    def start(self):
        self.generate_vm_files()
        self.game_loop()
        self.root.mainloop()

if __name__ == "__main__":
    HackEmulator().start()