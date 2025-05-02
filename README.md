
# Snake Game – OOP Coursework 2025

## Overview
This is a fully object-oriented implementation of the classic Snake game using Python and Tkinter.
The game features:
- Growing snake mechanics
- Randomly spawning food
- Special food types (regular,   double points, multi-spawn)
- Wall collision logic
- Score tracking and saving

##  How to Run

1. Make sure you have Python installed.
2. Run the game with:
   ```bash
   python snake_game.py
   ```
3. To run unit tests:
   ```bash
   python test_snake_imported.py
   ```

##  Object-Oriented Principles Used

###  Encapsulation
- Game logic is organized into classes like `Snake`, `Food`, `ScoreManager`, and `Game`.
- Each class manages its own state and behavior.

###  Abstraction
- Complex actions like moving, growing, checking collisions are abstracted into methods like `move()`, `grow()`, etc.

###  Inheritance
- All food types (`RegularFood`, `DoublePointFood`, `MultiSpawnFood`) inherit from `BaseFood`.

###  Polymorphism
- All food types implement the shared method `effect(game)` differently, allowing interchangeable behavior.

##  Design Pattern

- **Singleton Pattern** is used for the `Game` class to ensure only one instance of the game runs.

##  File I/O
- Scores are saved in `scores.txt` using JSON.
- Top 5 scores are read and displayed on game over screen.

##  Unit Testing

Unit tests are written using Python’s `unittest` module and are included in `test_snake_imported.py`.

- ✅ Test snake grows correctly
- ✅ Test snake moves and updates head
- ✅ Test collision with game boundaries
- ✅ Test score manager saves and sorts correctly

##  Screenshots

*(Insert gameplay screenshots here if needed)*

##  What I Learned

- How to use OOP principles to structure a real game
- How to apply the Singleton design pattern
- How to write and run unit tests
- How to use `Tkinter` for basic GUI

##  Conclusion

This project is a complete OOP-based game with game logic, UI, testing, and documentation. I’m proud of the result and see ways to improve it even further.

##  Possible Improvements

- Add sound effects
- Add levels and boss battle
- Add pause/resume functionality
- Add leaderboard with names
