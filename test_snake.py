
import unittest
import tempfile
import os
import json

from snake import Snake, ScoreManager, SPACE_SIZE, GAME_WIDTH, GAME_HEIGHT

class DummyCanvas:
    def create_rectangle(self, *args, **kwargs): pass
    def create_oval(self, *args, **kwargs): pass
    def create_text(self, *args, **kwargs): pass
    def create_window(self, *args, **kwargs): pass
    def delete(self, *args, **kwargs): pass

class TestSnakeGame(unittest.TestCase):
    def test_snake_grow(self):
        snake = Snake(DummyCanvas())
        original_length = snake.length
        snake.grow()
        self.assertEqual(snake.length, original_length + 1)

    def test_snake_move(self):
        snake = Snake(DummyCanvas())
        original_head = snake.head.copy()
        snake.move()
        self.assertNotEqual(snake.head, original_head)

    def test_snake_boundaries(self):
        snake = Snake(DummyCanvas())
        snake.head = [GAME_WIDTH, GAME_HEIGHT]  # Move snake out of bounds
        self.assertTrue(snake.check_collision())

    def test_score_manager(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name
        try:
            sm = ScoreManager(path)
            sm.save_score(5)
            sm.save_score(10)
            sm.save_score(20)
            self.assertEqual(sm.get_high_scores(), [20, 10, 5])
        finally:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
