from array import array
import math
import pygame


class SoundEffects:
    """Efeitos sintetizados com biblioteca padrão, sem arquivos externos."""

    def __init__(self):
        self.sounds = {}
        settings = pygame.mixer.get_init()
        if not settings or settings[1] != -16:
            return
        rate, _, channels = settings
        for name, frequency, duration in [('pickup', 880, .12), ('crash', 110, .3), ('shot', 660, .08)]:
            count = int(rate * duration)
            samples = array('h')
            for i in range(count):
                sample = int(4500 * (1 - i / count) * math.sin(2 * math.pi * frequency * i / rate))
                samples.extend([sample] * channels)
            self.sounds[name] = pygame.mixer.Sound(buffer=samples)

    def play(self, name):
        if name in self.sounds and pygame.mixer.get_init():
            self.sounds[name].play()
