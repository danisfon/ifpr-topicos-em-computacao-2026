import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import unittest
import tempfile
from pathlib import Path
import pygame
from game.core.scores import ScoreStore
from game.domain.animation import Animation
from game.phases.phase_1 import GameManager


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1280, 720))

    def setUp(self):
        self.game = GameManager(self.screen, pygame.time.Clock(), pygame.font.Font(None, 32), pygame.font.Font(None, 22))

    def test_animation_loop_and_end(self):
        frames = [pygame.Surface((2, 2)), pygame.Surface((2, 2))]
        loop = Animation(frames, 10)
        loop.update(.35)
        self.assertIs(loop.frame, frames[1])
        once = Animation(frames, 10, False)
        once.update(100)
        self.assertIs(once.frame, frames[-1])

    def test_effects_refresh_without_stacking(self):
        world = self.game.p1
        for _ in range(10):
            world._apply_consumable_effect('oleo')
            world._apply_consumable_effect('speed')
        self.assertEqual(world.car.MAX_SPEED, 270.0)
        world._update_active_effects(4)
        self.assertEqual(world.car.MAX_SPEED, 340.0)
        self.assertEqual(self.game.p2.car.MAX_SPEED, 340.0)

    def test_fractional_motion_and_render(self):
        car = self.game.p1.car
        self.assertIsInstance(car.size.x, float)
        initial = car.position.x
        car.velocity.x = 0.5
        car.update_motion(.1)
        self.assertAlmostEqual(car.position.x - initial, .05)
        self.game.p1.draw(self.screen, self.game.font, self.game.small_font)

    def test_match_saved_once_and_persists(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'scores.json'
            self.game.score_store = ScoreStore(path)
            self.game.p1.name = 'João'
            self.game.p1.survival_time = 12.5
            self.game.p1.alive = self.game.p2.alive = False
            self.game._update_result(.1)
            self.game._update_result(.1)
            rows = ScoreStore(path).read()
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['name'], 'João')
            self.assertEqual(rows[0]['score'], 125)

    def test_invalid_history_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'scores.json'
            path.write_text('invalid', encoding='utf-8')
            with self.assertRaises(ValueError):
                ScoreStore(path).save_match((self.game.p1, self.game.p2))
            self.assertEqual(path.read_text(), 'invalid')


if __name__ == '__main__':
    unittest.main()
