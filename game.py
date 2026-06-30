import tkinter as tk
import random
import math
import os

WIDTH = 900
HEIGHT = 600
ASSET_DIR = "assets"


class RS3PoliceChase:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RS3 Police Chase")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#1f1f1f")
        self.canvas.pack()

        self.screen = "menu"
        self.keys = set()
        self.difficulty = "Easy"
        self.game_running = False

        self.images = {}
        self.load_assets()

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.root.bind("<Button-1>", self.mouse_click)

        self.menu()
        self.root.mainloop()

    def asset_path(self, filename):
        return os.path.join(ASSET_DIR, filename)

    def load_image(self, filename, target_w=None, target_h=None):
        try:
            img = tk.PhotoImage(file=self.asset_path(filename))

            if target_w and target_h:
                x_scale = max(1, img.width() // target_w)
                y_scale = max(1, img.height() // target_h)
                scale = max(x_scale, y_scale)
                img = img.subsample(scale, scale)

            return img
        except Exception:
            return None

    def load_assets(self):
        self.images["rs3front"] = self.load_image("rs3front.png", 180, 120)
        self.images["rs3top"] = self.load_image("rs3top.png", 70, 120)
        self.images["police"] = self.load_image("police.png", 95, 55)
        self.images["road"] = self.load_image("road.png", WIDTH, HEIGHT)
        self.images["cashbag"] = self.load_image("cashbag.png", 45, 45)

    def clear(self):
        self.canvas.delete("all")

    def key_down(self, event):
        key = event.keysym
        self.keys.add(key)

        if key == "Escape":
            self.root.destroy()

        if self.screen == "game_over":
            if key.lower() == "r":
                self.start_game()
            elif key.lower() == "m":
                self.menu()

    def key_up(self, event):
        self.keys.discard(event.keysym)

    def button(self, x, y, text, tag):
        self.canvas.create_rectangle(
            x - 145, y - 30, x + 145, y + 30,
            fill="#111111",
            outline="white",
            width=3,
            tags=tag
        )
        self.canvas.create_text(
            x, y,
            text=text,
            fill="white",
            font=("Arial", 18, "bold"),
            tags=tag
        )

    def draw_background(self):
        if self.images["road"]:
            self.canvas.create_image(WIDTH // 2, HEIGHT // 2, image=self.images["road"])
        else:
            self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#202020", outline="")

            for x in range(0, WIDTH, 120):
                self.canvas.create_line(x, 0, x, HEIGHT, fill="#333333", width=3)

            for y in range(0, HEIGHT, 100):
                self.canvas.create_line(0, y, WIDTH, y, fill="#333333", width=3)

    def menu(self):
        self.screen = "menu"
        self.game_running = False
        self.clear()

        self.draw_background()
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black", stipple="gray50")

        self.canvas.create_text(
            WIDTH / 2, 65,
            text="RS3 POLICE CHASE",
            fill="white",
            font=("Arial", 38, "bold")
        )

        self.canvas.create_text(
            WIDTH / 2, 110,
            text="2D Arcade Driving Game",
            fill="#dddddd",
            font=("Arial", 17)
        )

        if self.images["rs3front"]:
            self.canvas.create_image(WIDTH / 2, 200, image=self.images["rs3front"])
        else:
            self.draw_simple_car(WIDTH / 2, 200, "cyan", "RS3")

        self.button(WIDTH / 2, 315, "PLAY", "play")
        self.button(WIDTH / 2, 385, "DIFFICULTY", "difficulty")
        self.button(WIDTH / 2, 455, "INSTRUCTIONS", "instructions")
        self.button(WIDTH / 2, 525, "EXIT", "exit")

    def instructions(self):
        self.screen = "instructions"
        self.clear()

        self.draw_background()
        self.canvas.create_rectangle(70, 50, WIDTH - 70, HEIGHT - 50, fill="#111111", outline="white", width=3)

        self.canvas.create_text(WIDTH / 2, 90, text="INSTRUCTIONS", fill="white", font=("Arial", 34, "bold"))

        lines = [
            "Use arrow keys or WASD to drive the RS3.",
            "Collect cash bags to increase your score.",
            "Avoid police cars or you will lose lives.",
            "You start with 3 lives.",
            "Try to get the highest score before the timer reaches zero.",
            "After game over, press R to restart or M for menu.",
            "Press Esc at any time to close the game."
        ]

        y = 150
        for line in lines:
            self.canvas.create_text(WIDTH / 2, y, text=line, fill="white", font=("Arial", 17))
            y += 40

        self.button(WIDTH / 2, 520, "BACK", "back")

    def difficulty_menu(self):
        self.screen = "difficulty"
        self.clear()

        self.draw_background()
        self.canvas.create_rectangle(100, 55, WIDTH - 100, HEIGHT - 55, fill="#111111", outline="white", width=3)

        self.canvas.create_text(WIDTH / 2, 95, text="CHOOSE DIFFICULTY", fill="white", font=("Arial", 34, "bold"))
        self.canvas.create_text(WIDTH / 2, 145, text=f"Current difficulty: {self.difficulty}", fill="#dddddd", font=("Arial", 16))

        self.button(WIDTH / 2, 230, "EASY", "easy")
        self.button(WIDTH / 2, 315, "MEDIUM", "medium")
        self.button(WIDTH / 2, 400, "HARD", "hard")
        self.button(WIDTH / 2, 510, "BACK", "back")

    def mouse_click(self, event):
        clicked = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        tags = []

        for item in clicked:
            tags += list(self.canvas.gettags(item))

        if "play" in tags:
            self.start_game()
        elif "difficulty" in tags:
            self.difficulty_menu()
        elif "instructions" in tags:
            self.instructions()
        elif "exit" in tags:
            self.root.destroy()
        elif "back" in tags:
            self.menu()
        elif "easy" in tags:
            self.difficulty = "Easy"
            self.start_game()
        elif "medium" in tags:
            self.difficulty = "Medium"
            self.start_game()
        elif "hard" in tags:
            self.difficulty = "Hard"
            self.start_game()
        elif "again" in tags:
            self.start_game()
        elif "menu" in tags:
            self.menu()

    def start_game(self):
        self.screen = "game"
        self.game_running = True
        self.clear()

        self.score = 0
        self.lives = 3
        self.time_left = 60
        self.timer_tick = 0

        self.player = {
            "x": WIDTH / 2,
            "y": HEIGHT / 2,
            "speed": 8
        }

        if self.difficulty == "Easy":
            police_count = 2
            police_speed = 2.2
        elif self.difficulty == "Medium":
            police_count = 4
            police_speed = 2.8
        else:
            police_count = 6
            police_speed = 3.4

        self.cash = []
        self.police = []

        for _ in range(7):
            self.cash.append(self.random_cash())

        for _ in range(police_count):
            self.police.append({
                "x": random.randint(60, WIDTH - 60),
                "y": random.randint(110, HEIGHT - 60),
                "speed": police_speed,
                "cooldown": 0
            })

        self.game_loop()

    def random_cash(self):
        return {
            "x": random.randint(60, WIDTH - 60),
            "y": random.randint(100, HEIGHT - 60)
        }

    def draw_simple_car(self, x, y, colour, label):
        self.canvas.create_rectangle(x - 28, y - 16, x + 28, y + 16, fill=colour, outline="white", width=2)
        self.canvas.create_rectangle(x - 16, y - 24, x + 16, y + 24, fill=colour, outline="white", width=2)
        self.canvas.create_text(x, y, text=label, fill="black", font=("Arial", 8, "bold"))

    def draw_player(self):
        if self.images["rs3top"]:
            self.canvas.create_image(self.player["x"], self.player["y"], image=self.images["rs3top"])
        else:
            self.draw_simple_car(self.player["x"], self.player["y"], "cyan", "RS3")

    def draw_police(self, p):
        if self.images["police"]:
            self.canvas.create_image(p["x"], p["y"], image=self.images["police"])
        else:
            colour = "gray" if p["cooldown"] > 0 else "red"
            self.draw_simple_car(p["x"], p["y"], colour, "POL")

    def draw_cash(self, c):
        if self.images["cashbag"]:
            self.canvas.create_image(c["x"], c["y"], image=self.images["cashbag"])
        else:
            self.canvas.create_rectangle(c["x"] - 14, c["y"] - 10, c["x"] + 14, c["y"] + 10, fill="#2ecc71", outline="white", width=2)
            self.canvas.create_text(c["x"], c["y"], text="£", fill="white", font=("Arial", 14, "bold"))

    def draw_hud(self):
        self.canvas.create_rectangle(0, 0, WIDTH, 70, fill="#111111", outline="")
        self.canvas.create_text(90, 35, text=f"Score: {self.score}", fill="white", font=("Arial", 18, "bold"))
        self.canvas.create_text(250, 35, text=f"Lives: {self.lives}", fill="white", font=("Arial", 18, "bold"))
        self.canvas.create_text(420, 35, text=f"Time: {self.time_left}", fill="white", font=("Arial", 18, "bold"))
        self.canvas.create_text(670, 35, text=f"Difficulty: {self.difficulty}", fill="white", font=("Arial", 18, "bold"))

    def distance(self, a, b):
        return math.hypot(a["x"] - b["x"], a["y"] - b["y"])

    def move_player(self):
        if "Left" in self.keys or "a" in self.keys:
            self.player["x"] -= self.player["speed"]
        if "Right" in self.keys or "d" in self.keys:
            self.player["x"] += self.player["speed"]
        if "Up" in self.keys or "w" in self.keys:
            self.player["y"] -= self.player["speed"]
        if "Down" in self.keys or "s" in self.keys:
            self.player["y"] += self.player["speed"]

        self.player["x"] = max(45, min(WIDTH - 45, self.player["x"]))
        self.player["y"] = max(95, min(HEIGHT - 45, self.player["y"]))

    def move_police(self):
        for i, p in enumerate(self.police):
            dx = self.player["x"] - p["x"]
            dy = self.player["y"] - p["y"]
            dist = math.hypot(dx, dy)

            if dist != 0:
                p["x"] += (dx / dist) * p["speed"]
                p["y"] += (dy / dist) * p["speed"]

            for j, other in enumerate(self.police):
                if i != j:
                    gap_x = p["x"] - other["x"]
                    gap_y = p["y"] - other["y"]
                    gap_dist = math.hypot(gap_x, gap_y)

                    if gap_dist < 60 and gap_dist != 0:
                        p["x"] += (gap_x / gap_dist) * 1.5
                        p["y"] += (gap_y / gap_dist) * 1.5

            if p["cooldown"] > 0:
                p["cooldown"] -= 1

    def check_collisions(self):
        for c in self.cash[:]:
            if self.distance(self.player, c) < 45:
                self.cash.remove(c)
                self.score += 10
                self.cash.append(self.random_cash())

        for p in self.police:
            if self.distance(self.player, p) < 55 and p["cooldown"] == 0:
                self.lives -= 1
                p["cooldown"] = 60
                self.player["x"] = WIDTH / 2
                self.player["y"] = HEIGHT / 2

                if self.lives <= 0:
                    self.game_over("You were caught by the police!")
                    return

    def update_timer(self):
        self.timer_tick += 1

        if self.timer_tick >= 30:
            self.timer_tick = 0
            self.time_left -= 1

        if self.time_left <= 0:
            self.game_over("Time ran out!")
            return

    def game_loop(self):
        if self.screen != "game" or not self.game_running:
            return

        self.move_player()
        self.move_police()
        self.check_collisions()

        if self.screen != "game":
            return

        self.update_timer()

        if self.screen != "game":
            return

        self.clear()
        self.draw_background()

        for c in self.cash:
            self.draw_cash(c)

        for p in self.police:
            self.draw_police(p)

        self.draw_player()
        self.draw_hud()

        self.root.after(33, self.game_loop)

    def game_over(self, reason):
        self.screen = "game_over"
        self.game_running = False
        self.clear()

        self.draw_background()
        self.canvas.create_rectangle(110, 70, WIDTH - 110, HEIGHT - 70, fill="#111111", outline="white", width=3)

        self.canvas.create_text(WIDTH / 2, 125, text="GAME OVER", fill="white", font=("Arial", 42, "bold"))
        self.canvas.create_text(WIDTH / 2, 185, text=reason, fill="#dddddd", font=("Arial", 18))
        self.canvas.create_text(WIDTH / 2, 245, text=f"Final Score: {self.score}", fill="white", font=("Arial", 28, "bold"))

        if self.images["rs3front"]:
            self.canvas.create_image(WIDTH / 2, 330, image=self.images["rs3front"])

        self.canvas.create_text(
            WIDTH / 2, 405,
            text="Press R to restart | Press M for menu | Press Esc to exit",
            fill="#dddddd",
            font=("Arial", 14)
        )

        self.button(WIDTH / 2, 465, "PLAY AGAIN", "again")
        self.button(WIDTH / 2, 535, "MAIN MENU", "menu")


RS3PoliceChase()