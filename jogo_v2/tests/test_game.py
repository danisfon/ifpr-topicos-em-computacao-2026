import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import unittest
import pygame
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


if __name__ == '__main__':
    unittest.main()
