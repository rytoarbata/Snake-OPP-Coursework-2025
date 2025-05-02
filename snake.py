from tkinter import *
import random
import json
import os
import time

# =========================
# CONFIGURABLE PARAMETERS
# =========================
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
DOUBLE_FOOD_COLOR = "#FFFF00"
MULTI_FOOD_COLOR = "#00FFFF"
BACKGROUND_COLOR = "#000000"
SCORE_FILE = "scores.txt"

def wall_art_pattern():
        # Return a list of wall coordinate pairs to form a face or shape
        pattern = [
            (5, 5), (6, 5), (7, 5),
            (5, 6), (5, 7), (5, 8),
            (7, 6), (7, 7), (7, 8), (6, 8),

            (9, 5), (10, 5), (11, 5),
            (9, 6), (9, 7), (9, 8),
            (11, 6), (11, 7), (11, 8), (10, 8),

            (13, 5), (13, 6), (13, 7), (13, 8),
            (14, 7), (14, 5), (15, 6), (15, 7), (15, 5)
        ]
        return [(x * SPACE_SIZE, y * SPACE_SIZE) for x, y in pattern]


def create_wall_art(canvas):
        return [Wall(canvas, [x, y]) for x, y in wall_art_pattern()] 

# =========================
# SINGLETON META
# =========================
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# =========================
# GAME CLASS
# =========================
class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake Game OOP")
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.snake = Snake(self.canvas)
        self.foods = [RegularFood(self.canvas)]
        self.score_manager = ScoreManager(SCORE_FILE)
        self.score = 0
        self.double_points_active = False
        self.double_points_end_time = 0
        self.blink = False
        self.current_speed = SPEED

        self.walls = create_wall_art(self.canvas)
        self.show_start_screen()

        self.running = True

        self.window.bind("<KeyPress>", self.change_direction)
        self.window.mainloop()

    def show_start_screen(self):
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 40,
                                fill="white", font="Arial 24 bold", text="SNAKE GAME")

        start_button = Button(self.window, text="Start Game", font="Arial 14",
                            command=self.start_game)
        
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 60,
                        fill="white", font="Arial 10", text="Use arrow keys to move")

        self.canvas.create_window(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 20, window=start_button)

        self.start_button = start_button  # Save reference so we can remove it later

    def start_game(self):
        self.start_button.destroy()  # Remove the start button

        # Initialize game state
        self.snake = Snake(self.canvas)
        self.foods = [RegularFood(self.canvas)]
        self.score = 0
        self.double_points_active = False
        self.current_speed = SPEED
        self.walls = create_wall_art(self.canvas)
        self.running = True

        self.canvas.delete("all")
        self.update_game()

    def change_direction(self, event):
        direction = event.keysym
        if direction in ['Up', 'Down', 'Left', 'Right']:
            self.snake.change_direction(direction.upper())

    def activate_double_points(self):
        self.double_points_active = True
        self.double_points_end_time = time.time() + 10
        self.current_speed = int(SPEED * 0.75)

    def deactivate_double_points(self):
        self.double_points_active = False
        self.current_speed = SPEED

    def update_game(self):
        if not self.running:
            return  # Stop updating if game is over

        if time.time() >= self.double_points_end_time:
            self.deactivate_double_points()

        # Remove expired temporary foods
        for food in self.foods[:]:
            if isinstance(food, TemporaryFood) and food.is_expired():
                self.foods.remove(food)

        # Move the snake
        if self.snake.move():
            # Check for wall collisions IMMEDIATELY after move
            if self.snake.check_collision_with_walls(self.walls) or self.snake.check_collision():
                self.show_game_over()
                return  # Exit without drawing

            # Check if snake eats any food
            for food in self.foods[:]:
                if self.snake.head == food.position:
                    score_gained = food.effect(self)
                    self.score += score_gained
                    self.foods.remove(food)

                    # Add new food (random type)
                    new_food = random.choice([RegularFood, DoublePointFood, MultiSpawnFood])
                    self.foods.append(new_food(self.canvas))

            # === DRAWING SECTION ===
            self.canvas.delete("all")  # Clear the canvas for redrawing

            self.snake.draw()  # Draw snake
            for food in self.foods:
                food.draw()
            for wall in self.walls:
                wall.draw()

            # Score display
            if self.double_points_active:
                self.blink = not self.blink
                color = "yellow" if self.blink else "white"
            else:
                color = "white"
            self.canvas.create_text(70, 20, fill=color, font="Arial 20 bold", text=f"Score: {self.score}")

            # Schedule next update
            self.window.after(self.current_speed, self.update_game)
        else:
            # Snake hit itself or boundary (already checked)
            self.show_game_over()
            return

     

    def show_game_over(self):
        self.running = False
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, fill="red", font="Arial 20 bold", text="WHOMP WHOMP")
        self.score_manager.save_score(self.score)
        scores = self.score_manager.get_high_scores()
        score_text = "High Scores:\n" + "\n".join(str(s) for s in scores)
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 60, fill="white", font="Arial 12", text=score_text)

        # Add Restart Button
        restart_button = Button(self.window, text="Restart", command=self.restart_game)
        self.canvas.create_window(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 100, window=restart_button)

    def restart_game(self):
        # Reset game state
        self.snake = Snake(self.canvas)
        self.foods = [RegularFood(self.canvas)]
        self.score = 0
        self.double_points_active = False
        self.current_speed = SPEED
        self.walls = create_wall_art(self.canvas)
        self.running = True
        self.canvas.delete("all")
        self.update_game()


# =========================
# SNAKE CLASS
# =========================
class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [[GAME_WIDTH // 2, GAME_HEIGHT // 2]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.head = self.body[0]
        self.length = BODY_PARTS

        for _ in range(1, BODY_PARTS):
            self.body.append([self.body[-1][0] - SPACE_SIZE, self.body[-1][1]])

    def change_direction(self, dir):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if dir != opposite_directions.get(self.direction):
            self.change_to = dir

    def move(self):
        x, y = self.head
        if self.change_to == 'UP':
            y -= SPACE_SIZE
        if self.change_to == 'DOWN':
            y += SPACE_SIZE
        if self.change_to == 'LEFT':
            x -= SPACE_SIZE
        if self.change_to == 'RIGHT':
            x += SPACE_SIZE
        self.direction = self.change_to
        self.head = [x, y]
        self.body.insert(0, self.head.copy())
        if len(self.body) > self.length:
            self.body.pop()

        if self.check_collision() or self.check_self_collision():
            return False
        return True

    def grow(self):
        self.length += 1

    def check_collision(self):
        x, y = self.head
        return x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT

    def check_self_collision(self):
        return self.head in self.body[1:]
    
    def check_collision_with_walls(self, walls):
        for wall in walls:
            if self.head == wall.position:
                return True
        return False


    def draw(self):
        for x, y in self.body:
            self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

# =========================
# BASE FOOD CLASS
# =========================
class BaseFood:
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = SPACE_SIZE
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (GAME_WIDTH - self.size) // self.size) * self.size
        y = random.randint(0, (GAME_HEIGHT - self.size) // self.size) * self.size
        return [x, y]

    def effect(self, game):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

# =========================
# FOOD TYPES
# =========================
class RegularFood(BaseFood):
    def effect(self, game):
        game.snake.grow()
        return 1 if not game.double_points_active else 2

    def draw(self):
        x, y = self.position
        self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=FOOD_COLOR)

class DoublePointFood(BaseFood):
    def effect(self, game):
        game.snake.grow()
        game.activate_double_points()
        return 2

    def draw(self):
        x, y = self.position
        self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=DOUBLE_FOOD_COLOR)

class MultiSpawnFood(BaseFood):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.spawn_time = time.time()
        self.blink_state = True  # For blinking

    def effect(self, game):
        game.snake.grow()
        for _ in range(3):
            game.foods.append(TemporaryFood(game.canvas))
        return 3 if not game.double_points_active else 6

    def draw(self):
        # Blinking logic
        current_time = time.time()
        if int(current_time * 5) % 2 == 0:  # Blink every 0.5 seconds
            x, y = self.position
            self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=MULTI_FOOD_COLOR)

class TemporaryFood(RegularFood):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.spawn_time = time.time()

    def draw(self):
        current_time = time.time()
        if int(current_time * 5) % 2 == 0:
            x, y = self.position
            self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=FOOD_COLOR)

    def is_expired(self):
        return time.time() - self.spawn_time > 4

# =========================
# SCORE MANAGER
# =========================
class ScoreManager:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def save_score(self, score):
        try:
            with open(self.filename, 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
        scores.append(score)
        with open(self.filename, 'w') as f:
            json.dump(scores, f)

    def get_high_scores(self):
        with open(self.filename, 'r') as f:
            return sorted(json.load(f), reverse=True)[:5]

class Wall:
    def __init__(self, canvas, position):
        self.canvas = canvas
        self.position = position  # [x, y]
        self.size = SPACE_SIZE

    def draw(self):
        x, y = self.position
        self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="grey")

# =========================
# START GAME
# =========================
if __name__ == "__main__":
    game = Game()
