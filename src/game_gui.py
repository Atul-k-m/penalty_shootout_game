import tkinter as tk
import numpy as np
import random
import math
import joblib
from tkinter import messagebox, ttk

class SmoothAnimator:
 
    @staticmethod
    def parabolic_trajectory(start, end, steps=30):
     
        trajectory = []
        for t in np.linspace(0, 1, steps):
  
            height = 4 * math.sin(t * math.pi)
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t + height * 50
            trajectory.append((x, y))
        return trajectory

class PenaltyShootoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Penalty Shootout Simulator")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e2e') 

        # Game state tracking
        self.power_var = tk.DoubleVar(value=5)
        self.angle_var = tk.DoubleVar(value=0)
        self.goals = 0
        self.attempts = 0
        self.round = 0
        self.max_rounds = 500
        self.difficulty_factor = 0.7

  
        try:
            model_data = joblib.load('../models/advanced_goalkeeper_model.pkl')
            self.model = model_data['model']
            self.scaler = model_data['scaler']
        except FileNotFoundError:
            messagebox.showerror("Model Error", "Machine learning model not found. Please train the model first.")
            self.root.quit()
            return

   
        self.main_frame = tk.Frame(root, bg='#1e1e2e')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

       
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(
            self.main_frame, 
            width=self.canvas_width, 
            height=self.canvas_height, 
            bg='#2ecc71', 
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        
        self.draw_stadium()


        self.goal_width = 300
        self.goal_height = 200
        self.goal_x = (self.canvas_width - self.goal_width) // 2
        self.goal_y = 50

       
        self.draw_goal()


        self.reset_ball_and_goalkeeper()

       
        self.setup_controls()

  
        self.setup_stats_frame()


        self.canvas.bind("<Button-1>", self.prepare_shot)

    def reset_ball_and_goalkeeper(self):
       
       
        self.ball_radius = 15
        self.ball = self.canvas.create_oval(
            self.canvas_width // 2 - self.ball_radius, 
            self.canvas_height - 50 - self.ball_radius,
            self.canvas_width // 2 + self.ball_radius, 
            self.canvas_height - 50 + self.ball_radius,
            fill='white', outline='black'
        )
        
        # Goalkeeper reset
        self.goalkeeper_width = 50
        self.goalkeeper_height = 80
        self.goalkeeper_initial_x = self.goal_x + self.goal_width // 2 - self.goalkeeper_width // 2
        self.goalkeeper_initial_y = self.goal_y
        self.goalkeeper = self.canvas.create_rectangle(
            self.goalkeeper_initial_x,
            self.goalkeeper_initial_y,
            self.goalkeeper_initial_x + self.goalkeeper_width,
            self.goalkeeper_initial_y + self.goalkeeper_height,
            fill='blue', outline='white'
        )

    def setup_stats_frame(self):
       
        stats_frame = tk.Frame(self.main_frame, bg='#1e1e2e')
        stats_frame.pack(pady=10)

       
        self.rounds_label = tk.Label(
            stats_frame, 
            text=f"Round: {self.round}/{self.max_rounds}", 
            font=("Arial", 14),
            bg='#1e1e2e',
            fg='white'
        )
        self.rounds_label.pack(side=tk.LEFT, padx=10)

        
        self.stats_label = tk.Label(
            stats_frame, 
            text="Goals: 0 | Attempts: 0 | Success Rate: 0%", 
            font=("Arial", 14),
            bg='#1e1e2e',
            fg='white'
        )
        self.stats_label.pack(side=tk.LEFT, padx=10)

    def draw_stadium(self):
      
        for x in range(0, self.canvas_width, 20):
            for y in range(0, self.canvas_height, 20):
                shade = random.uniform(0.8, 1.2)
                green = int(min(46 * shade, 255))
                self.canvas.create_rectangle(x, y, x+20, y+20, 
                                             fill=f'#{green:02x}cc71', 
                                             outline='')

       
        for x in range(0, self.canvas_width, 50):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill='white', width=1)

     
        for y in range(self.canvas_height-100, self.canvas_height, 20):
            for x in range(0, self.canvas_width, 30):
                color = random.choice(['#34495e', '#2c3e50', '#7f8c8d'])
                self.canvas.create_rectangle(x, y, x+20, y+10, fill=color, outline='')

    def draw_goal(self):
       
        self.canvas.create_rectangle(
            self.goal_x, self.goal_y, 
            self.goal_x + self.goal_width, 
            self.goal_y + self.goal_height, 
            fill='', outline='white', width=3
        )
        
    
        net_color = '#bdc3c7'
        for i in range(10):
           
            self.canvas.create_line(
                self.goal_x + i * (self.goal_width // 10) + random.randint(-2, 2), 
                self.goal_y,
                self.goal_x + i * (self.goal_width // 10) + random.randint(-2, 2), 
                self.goal_y + self.goal_height,
                fill=net_color, width=1
            )
       
            self.canvas.create_line(
                self.goal_x, 
                self.goal_y + i * (self.goal_height // 10) + random.randint(-2, 2),
                self.goal_x + self.goal_width, 
                self.goal_y + i * (self.goal_height // 10) + random.randint(-2, 2),
                fill=net_color, width=1
            )

    def setup_controls(self):
        
        control_frame = tk.Frame(self.main_frame, bg='#1e1e2e')
        control_frame.pack(pady=10)
        
     
        power_frame = tk.Frame(control_frame, bg='#1e1e2e')
        power_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(power_frame, text="Shot Power:", bg='#1e1e2e', fg='white').pack()
        power_slider = ttk.Scale(
            power_frame, 
            from_=1, to=10, 
            orient=tk.HORIZONTAL, 
            length=200, 
            variable=self.power_var
        )
        power_slider.pack()
        
   
        angle_frame = tk.Frame(control_frame, bg='#1e1e2e')
        angle_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(angle_frame, text="Shot Angle:", bg='#1e1e2e', fg='white').pack()
        angle_slider = ttk.Scale(
            angle_frame, 
            from_=-45, to=45, 
            orient=tk.HORIZONTAL, 
            length=200, 
            variable=self.angle_var
        )
        angle_slider.pack()

    def check_collision(self, ball_coords, goalkeeper_coords):
        
        ball_x1, ball_y1, ball_x2, ball_y2 = ball_coords
        gk_x1, gk_y1, gk_x2, gk_y2 = goalkeeper_coords
        
    
        return not (ball_x2 < gk_x1 or ball_x1 > gk_x2 or 
                    ball_y2 < gk_y1 or ball_y1 > gk_y2)

    def prepare_shot(self, event):
       
        if event.y > self.canvas_height - 100 or event.y < self.goal_y:
            messagebox.showwarning("Invalid Shot", "Shoot towards the goal!")
            return
        
     
        if self.round >= self.max_rounds:
            messagebox.showinfo("Game Over", f"Final Score: {self.goals}/{self.max_rounds}")
            return

   
        self.canvas.coords(
            self.ball, 
            self.canvas_width // 2 - self.ball_radius, 
            self.canvas_height - 50 - self.ball_radius,
            self.canvas_width // 2 + self.ball_radius, 
            self.canvas_height - 50 + self.ball_radius
        )

        
        self.canvas.coords(
            self.goalkeeper,
            self.goalkeeper_initial_x,
            self.goalkeeper_initial_y,
            self.goalkeeper_initial_x + self.goalkeeper_width,
            self.goalkeeper_initial_y + self.goalkeeper_height
        )
        
 
        power = self.power_var.get()
        angle = self.angle_var.get()
        
   
        goalkeeper_features = np.array([
            event.x, event.y, power, angle, 
            random.uniform(0, 10),  
            random.uniform(100, 500)  
        ]).reshape(1, -1)
      
        goalkeeper_features_scaled = self.scaler.transform(goalkeeper_features)
        goal_prob = self.model.predict_proba(goalkeeper_features_scaled)[0][1]
      
        goal_prob *= self.difficulty_factor
        
        is_goal = random.random() < goal_prob
        
       
        if (event.x < self.goal_x or event.x > self.goal_x + self.goal_width):
            is_goal = False
            messagebox.showinfo("Miss!", "You shot wide of the goal!")
        
       
        target_x = event.x + angle * 5
        target_y = event.y
        
        
        self.animate_goalkeeper_dive(is_goal, target_x, target_y)
        
       
        start_pos = (self.canvas_width // 2, self.canvas_height - 50)
        end_pos = (target_x, target_y)
        self.animate_ball_trajectory(start_pos, end_pos, is_goal)
        
        
        self.attempts += 1
        self.round += 1
        if is_goal:
            self.goals += 1
        
        self.update_stats()

    def animate_goalkeeper_dive(self, is_goal, target_x, target_y):
       
        gk_center_x = self.goal_x + self.goal_width // 2
        dive_direction = 1 if target_x > gk_center_x else -1
        
        
        dive_offset = random.uniform(-30, 30)
        
     
        dive_steps = 20
        for i in range(dive_steps):
       
            offset_x = dive_direction * (i ** 2) * 0.5 + dive_offset
            offset_y = (i ** 2) * 0.3
            self.canvas.after(
                20 * i, 
                lambda x=offset_x, y=offset_y: self.canvas.move(self.goalkeeper, x, y)
            )

    def animate_ball_trajectory(self, start_pos, end_pos, is_goal):
        
        trajectory = SmoothAnimator.parabolic_trajectory(start_pos, end_pos)
        
        def animate_ball(index):
            if index < len(trajectory):
                x, y = trajectory[index]
             
                ball_coords = (
                    x - self.ball_radius, y - self.ball_radius,
                    x + self.ball_radius, y + self.ball_radius
                )
                self.canvas.coords(
                    self.ball, 
                    *ball_coords
                )
                
                
                gk_coords = self.canvas.coords(self.goalkeeper)
                is_collision = self.check_collision(ball_coords, gk_coords)
                
               
                if is_collision and is_goal:
                    is_goal = False
                
                self.root.after(20, lambda: animate_ball(index + 1))
            else:

                result = "GOAL!" if is_goal else "SAVED!"
                color = "green" if is_goal else "red"
                self.show_result(result, color)
        
        animate_ball(0)

    def update_stats(self):
        
        success_rate = (self.goals / self.attempts * 100) if self.attempts > 0 else 0
        self.stats_label.config(
            text= f"Goals: {self.goals} | Attempts: {self.attempts} | Success Rate: {success_rate:.2f}%"
        )
        self.rounds_label.config(
            text=f"Round: {self.round}/{self.max_rounds}"
        )

        
        if self.round >= self.max_rounds:
            result_message = f"Game Over!\nFinal Score: {self.goals}/{self.max_rounds}"
            messagebox.showinfo("Game Completed", result_message)

    def show_result(self, result, color):
        result_label = tk.Label(
            self.main_frame, 
            text=result, 
            font=("Arial", 24, "bold"), 
            fg=color,
            bg='#1e1e2e'
        )
        result_label.pack()
        self.root.after(1500, result_label.destroy)

    def adjust_difficulty(self, difficulty):
      
        if difficulty == "easy":
            self.difficulty_factor = 0.8
        elif difficulty == "medium":
            self.difficulty_factor = 0.7
        elif difficulty == "hard":
            self.difficulty_factor = 0.5
        else:
            self.difficulty_factor = 0.7

def main():
    root = tk.Tk()
    game = PenaltyShootoutGame(root)
    

    def create_difficulty_menu():
        difficulty_window = tk.Toplevel(root)
        difficulty_window.title("Select Difficulty")
        difficulty_window.geometry("300x200")
        
        tk.Label(difficulty_window, text="Select Game Difficulty", font=("Arial", 14)).pack(pady=10)
        
        difficulties = [
            ("Easy (More Likely to Score)", "easy"),
            ("Medium (Balanced)", "medium"),
            ("Hard (More Challenging)", "hard")
        ]
        
        selected_difficulty = tk.StringVar(value="medium")
        
        for text, mode in difficulties:
            tk.Radiobutton(
                difficulty_window, 
                text=text, 
                variable=selected_difficulty, 
                value=mode
            ).pack(pady=5)
        
        def set_difficulty():
            game.adjust_difficulty(selected_difficulty.get())
            difficulty_window.destroy()
        
        tk.Button(
            difficulty_window, 
            text="Start Game", 
            command=set_difficulty
        ).pack(pady=10)
    

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    game_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Game", menu=game_menu)
    game_menu.add_command(label="Change Difficulty", command=create_difficulty_menu)
    game_menu.add_separator()
    game_menu.add_command(label="Exit", command=root.quit)
    
    root.mainloop()

if __name__ == "__main__":
    main()