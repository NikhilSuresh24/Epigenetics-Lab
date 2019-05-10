import simulator as sim
import tkinter as tk
import random

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.canvas = tk.Canvas(self, width=800, height=670)
        self.canvas.pack()

        self.control_frame = tk.Frame(self, width=250, height=200)
        self.control_frame.pack(side=tk.RIGHT)

        self.new_state_button = tk.Button(self.control_frame, text="New State", command=self.new_state)
        self.new_state_button.pack(side=tk.LEFT)

        self.step_button = tk.Button(self.control_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.LEFT)

        self.sim = sim.Simulator(False)
            
    def new_state(self):
        v = [float(random.randint(-1, 1)) for _ in range(10)]
        self.sim.reset(v, [1.0 if x >= 0 else 0.0 for x in v])
        self.history = [(self.sim.get_v(), self.sim.get_x())]
        self.draw_state()

    def step(self):
        self.sim.step()
        self.history.append((self.sim.get_v(), self.sim.get_x()))
        self.draw_state()

    def draw_state(self):
        phenotype = self.sim.print_state()

        self.canvas.delete("all")
        center_width = self.canvas.winfo_width()/2
        center_height = self.canvas.winfo_height()/2
        
        text_y = 50

        self.canvas.create_text(30, text_y, anchor="w", text="head size body eyes wm// rm// em// wa// ra// ea//")

        for v,x in self.history:
            text_y += 20
            self.canvas.create_text(15, text_y, anchor="w", text="v: ")
            rect_x = 0
            for i in v:
                rect_x += 33
                color = "white"
                if i == -1:
                    color = "red"
                elif i == 1:
                    color = "green"
                self.canvas.create_rectangle(rect_x, text_y, rect_x + 20, text_y + 10, fill=color)
            text_y += 20
            self.canvas.create_text(15, text_y, anchor="w", text="x: ")
            rect_x = 0
            for i in x:
                rect_x += 33
                color = "red"
                if i == 1:
                    color = "green"
                self.canvas.create_rectangle(rect_x, text_y, rect_x + 20, text_y + 10, fill=color)
            text_y += 20

        head_color = "white"
        if phenotype[0] == "R":
            head_color = "red"

        self.canvas.create_oval(center_width - 20, center_height - 100, center_width + 20, center_height - 50, fill=head_color)

        eye_color = "brown"
        if phenotype[3] == "B":
            eye_color = "blue"
        self.canvas.create_oval(center_width - 15, center_height - 90, center_width - 5, center_height - 80, fill=eye_color)
        self.canvas.create_oval(center_width + 15, center_height - 90, center_width + 5, center_height - 80, fill=eye_color)

        body_color = "purple"
        if phenotype[2] == "Q":
            body_color = "blue"

        if phenotype[1] == "W":
            self.canvas.create_oval(center_width - 30, center_height - 50, center_width + 30, center_height + 100, fill=body_color)
            
            self.canvas.create_line(center_width - 20, center_height, center_width - 90, center_height - 20, fill=body_color, width=5)
            self.canvas.create_line(center_width + 20, center_height, center_width + 90, center_height - 20, fill=body_color, width=5)

            self.canvas.create_line(center_width - 20, center_height + 80, center_width - 50, center_height + 150, fill=body_color, width=5)
            self.canvas.create_line(center_width + 20, center_height + 80, center_width + 50, center_height + 150, fill=body_color, width=5)
        else:
            self.canvas.create_line(center_width, center_height - 50, center_width, center_height + 100, fill=body_color, width=5)

            self.canvas.create_line(center_width, center_height, center_width - 90, center_height - 20, fill=body_color, width=5)
            self.canvas.create_line(center_width, center_height, center_width + 90, center_height - 20, fill=body_color, width=5)

            self.canvas.create_line(center_width, center_height + 100, center_width - 50, center_height + 150, fill=body_color, width=5)
            self.canvas.create_line(center_width, center_height + 100, center_width + 50, center_height + 150, fill=body_color, width=5)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()