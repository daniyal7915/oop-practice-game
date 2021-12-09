from abc import ABC, abstractmethod
import pygame
import Service
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display, object_):
        display.blit(object_.sprite, object_.position)


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        super().__init__()
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        # self.max_hp = 5 + self.stats["endurance"] * 2
        self.max_hp = 0
        for key in self.stats.keys():
            if key in ("strength", "endurance", "intelligence", "luck"):
                self.max_hp += self.stats[key]


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [60, 60]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.exp = xp

    def interact(self, engine, hero):
        hero.hp = hero.hp - self.hp
        if hero.hp <= 0:
            Service.reload_game(engine, hero)
        else:
            hero.exp += self.exp/2
            if hero.exp >= 100:
                hero.hp += 20
                if hero.hp > hero.max_hp:
                    hero.hp = hero.max_hp
                hero.exp = 0


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


# FIXME add classes - fixed

class Berserk(Effect):
    def apply_effect(self):
        for stat in self.stats.keys():
            if stat in ("strength", "endurance", "luck"):
                self.stats[stat] += 7
            else:
                self.stats[stat] -= 3
        self.hp += 50


class Blessing(Effect):
    def apply_effect(self):
        for stat in self.stats.keys():
            self.stats[stat] += 2


class Weakness(Effect):
    def apply_effect(self):
        for stat in self.stats.keys():
            self.stats[stat] -= 2


class Coffee(Effect):
    def apply_effect(self):
        self.hp += 10



