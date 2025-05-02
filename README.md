
# Snake Game – OOP Coursework 2025

## Introduction

This project is a Python implementation of the classic Snake game using the `tkinter` GUI library.
The goal of the coursework is to demonstrate all **4 OOP principles**, apply a **design pattern**, perform **file I/O**, and write **unit tests** in a fully functional Python application.

### How to Run the Program

1. Install Python 3.
2. Run the main game file:
3. Controls:
   - Use arrow keys to move the snake.
   - Collect food, avoid walls and your own tail.
4. Run unit tests:


## Body / Analysis

### Object-Oriented Programming Principles

#### 1. **Encapsulation**
> Hides internal data and logic within classes.

- Each class (`Snake`, `Food`, `Game`, `ScoreManager`) manages its own behavior.
- Example:
```python
class Snake:
    def __init__(self, canvas):
        self.body = [...]
        self.direction = 'RIGHT'
```

#### 2. **Abstraction**
> Simplifies usage by hiding complexity.

- Public methods like `snake.move()` and `snake.grow()` hide the logic of movement and growth.

#### 3. **Inheritance**
> Allows classes to reuse and extend functionality.

- Food types (`RegularFood`, `DoublePointFood`, `MultiSpawnFood`) all inherit from `BaseFood`.
```python
class RegularFood(BaseFood):
    def effect(self, game):
        ...
```

#### 4. **Polymorphism**
> Same interface, different behavior.

- All food types use the `effect(game)` method, but behave differently:
```python
food.effect(game)  # Could grow, spawn more food, or increase score differently
```

### Design Pattern: Singleton

- The `Game` class is implemented using the **Singleton Pattern** to ensure only one instance runs:
```python
class SingletonMeta(type):
    ...
class Game(metaclass=SingletonMeta):
    ...
```
- **Why Singleton?**: It ensures centralized control of the game loop and window, which is ideal for GUI applications.

###  Composition

- The `Game` class **uses composition** to hold and manage other objects:
    - `Snake`, `Food`, `ScoreManager`, `Wall`
- Example:
```python
class Game:
    def __init__(self):
        self.snake = Snake(canvas)
        self.foods = [RegularFood(canvas)]
        self.score_manager = ScoreManager("scores.txt")
```

### File I/O

- Scores are saved to and loaded from a `.txt` file using the `json` module.
- This persists data across game sessions.
```python
with open('scores.txt', 'w') as f:
    json.dump(scores, f)
```

### Unit Testing

- Core functions are tested using Python’s `unittest` framework.
- Covered functionality:
    - Snake growth
    - Snake movement
    - Boundary collision
    - ScoreManager save/load and sort
- Tests are located in:
```
test_snake_imported.py
```

### Code Style

- The code is written in **Python** and follows **PEP8** style:
    - Proper indentation
    - Snake_case variables
    - Logical organization of classes and methods

---

## Results

- ✅ Fully working Snake game with multiple food types and wall collisions.
- ✅ Successfully implemented and tested Singleton pattern and OOP pillars.
- ✅ Game saves high scores and displays top 5 on game over.
- ✅ Learned how to write unit tests to validate critical game logic.
- ✅ GUI built using `tkinter`.

---

##  Conclusions

This coursework demonstrates that a full game can be built and maintained using clean object-oriented principles in Python.
It uses encapsulation, inheritance, polymorphism, and abstraction throughout its structure, applies the Singleton pattern, and saves progress via file I/O.
Unit testing gave confidence in core functionality and structure.

### Future Improvements

- Add sound effects or music
- Add difficulty levels or increasing speed
- Add pause/resume buttons
- Add player names and global leaderboard
- Split code into modules for clarity

---

_Report created by Pavilas Šlapkauskas EF-24/2