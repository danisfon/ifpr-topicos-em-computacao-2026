import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import unittest
import tempfile
from pathlib import Path
import pygame
from game.core.scores import ScoreStore
from game.domain.entities import Obstacle
from game.domain.weapons import SPRITES
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
            self.game.p1.coins_collected = 3
            self.game.p1.alive = self.game.p2.alive = False
            self.game._update_result(.1)
            self.game._update_result(.1)
            rows = ScoreStore(path).read()
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['name'], 'João')
            self.assertEqual(rows[0]['score'], 30)

    def test_invalid_history_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'scores.json'
            path.write_text('invalid', encoding='utf-8')
            with self.assertRaises(ValueError):
                ScoreStore(path).save_match((self.game.p1, self.game.p2))
            self.assertEqual(path.read_text(), 'invalid')

    def test_weapon_cooldown_and_hit(self):
        world = self.game.p1
        projectile = world.weapon.fire(world.car)
        self.assertIsNone(world.weapon.fire(world.car))
        world.weapon.update(.4)
        self.assertIsNotNone(world.weapon.fire(world.car))
        obstacle = Obstacle(projectile.position.x + 40, projectile.position.y, 70, 100, 180, str(SPRITES / 'obstaculo.png'))
        world.obstacles.append(obstacle)
        world.projectiles.append(projectile)
        world._update_projectiles(.1)
        self.assertEqual(world.score, 0)
        self.assertEqual(world.projectiles, [])
        self.assertEqual(world.obstacles, [])
        world._update_projectiles(.1)
        self.assertEqual(world.score, 0)

    def test_coins_give_ten_points_once_and_only_to_collector(self):
        world = self.game.p1
        world.survival_time = 100.0
        self.assertEqual(world.score, 0)
        for count in range(1, 4):
            world._spawn_coin()
            coin = world.items[-1]
            coin.position.x, coin.position.y = world.car.position.x, world.car.position.y
            world._resolve_collisions()
            self.assertNotIn(coin, world.items)
            self.assertEqual(world.score, count * 10)
            world._resolve_collisions()
            self.assertEqual(world.score, count * 10)
        self.assertEqual(self.game.p2.score, 0)
        for effect in ('speed', 'shield', 'oleo'):
            world._apply_consumable_effect(effect)
        self.assertEqual(world.score, 30)
        self.game.p1, self.game.p2 = self.game._create_players()
        self.assertEqual(self.game.p1.score, 0)

    def test_coin_spawn_movement_and_offscreen_cleanup(self):
        from collections import defaultdict
        world = self.game.p1
        world._obstacle_spawn_timer = 100.0
        world._coin_spawn_timer = 0.0
        world.update(.01, defaultdict(bool))
        coin = next(item for item in world.items if item.effect == 'coin')
        self.assertGreaterEqual(coin.position.y, world.track_rect.top)
        self.assertLessEqual(coin.position.y + coin.size.y, world.track_rect.bottom)
        before = coin.position.x
        world.update(.01, defaultdict(bool))
        self.assertLess(coin.position.x, before)
        coin.position.x = world.track_rect.left - 100.0
        world.update(.01, defaultdict(bool))
        self.assertNotIn(coin, world.items)
        self.assertEqual(world.score, 0)

    def test_dead_player_cannot_fire(self):
        from collections import defaultdict
        world = self.game.p1
        world.alive = False
        world.update(.1, defaultdict(lambda: True))
        self.assertEqual(world.projectiles, [])

    def test_shield_consumed_then_next_collision_eliminates(self):
        world = self.game.p1
        def obstacle():
            return Obstacle(world.car.position.x, world.car.position.y, 70, 100, 180, str(SPRITES / 'obstaculo.png'))
        world.car.has_shield = True
        world.obstacles.append(obstacle())
        world._resolve_collisions()
        self.assertTrue(world.alive)
        self.assertFalse(world.car.has_shield)
        world.obstacles.append(obstacle())
        world._resolve_collisions()
        self.assertFalse(world.alive)
        self.assertTrue(world.car.damaged)

    def test_finish_returns_to_menu(self):
        self.game.p1.alive = self.game.p2.alive = False
        self.game._finish_timer = 10.0
        pygame.event.clear()
        self.assertEqual(self.game.run(), 'menu')

    def test_names_and_history_navigation(self):
        from game.interface.scores import ScoreScreens
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        screens = ScoreScreens(self.screen, pygame.time.Clock(), self.game.small_font, ScoreStore(Path(directory.name) / 'scores.json'))
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.TEXTINPUT, text='Ana'))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        pygame.event.post(pygame.event.Event(pygame.TEXTINPUT, text='João'))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual(screens.names(), ('Ana', 'João'))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.assertEqual(screens.history(), 'menu')

    def test_names_are_unique_and_reserved_without_a_match(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ScoreStore(Path(directory) / 'scores.json')
            self.assertTrue(any(store.validate_names([' Ana ', 'ANA'], [])))
            self.assertTrue(any(store.validate_names(['  ', 'Bia'], [])))
            self.assertEqual(store.register_names([' Ana ', 'João']), ('Ana', 'João'))
            reloaded = ScoreStore(store.path)
            with self.assertRaises(ValueError):
                reloaded.register_names(['ana', 'Bia'])
            self.assertFalse(store.path.exists())
            self.assertEqual(reloaded.registered_names(), ['Ana', 'João'])

    def test_history_names_cannot_be_registered_again(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ScoreStore(Path(directory) / 'scores.json')
            self.game.p1.name = 'Ana Maria'
            store.save_match((self.game.p1, self.game.p2))
            with self.assertRaises(ValueError):
                store.register_names(['  ANA   MARIA ', 'Bia'])

    def test_driving_frames_keep_silhouette_still(self):
        car = self.game.p1.car
        frames = car.animations.animations['driving'].sprites
        expected = pygame.mask.from_surface(car.sprite.surface)
        for frame in frames:
            actual = pygame.mask.from_surface(frame)
            self.assertEqual(actual.count(), expected.count())
            self.assertEqual(actual.overlap_area(expected, (0, 0)), expected.count())


if __name__ == '__main__':
    unittest.main()
