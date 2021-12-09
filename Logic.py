import Service


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    show_minimap = False

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        step = self.hero.sprite.get_width()
        for obj in self.objects:
            coords = []
            for coord in self.hero.position:
                coords.append(coord//step)
            if list(obj.position) == coords:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        step = self.hero.sprite.get_width()
        self.score -= 0.02
        if self.map[self.hero.position[1]//step - 1][self.hero.position[0]//step] == Service.wall:
            return
        self.hero.position[1] -= step
        self.interact()

    def move_down(self):
        step = self.hero.sprite.get_width()
        self.score -= 0.02
        if self.map[self.hero.position[1]//step + 1][self.hero.position[0]//step] == Service.wall:
            return
        self.hero.position[1] += step
        self.interact()

    def move_left(self):
        step = self.hero.sprite.get_width()
        self.score -= 0.02
        if self.map[self.hero.position[1]//step][self.hero.position[0]//step - 1] == Service.wall:
            return
        self.hero.position[0] -= step
        self.interact()

    def move_right(self):
        step = self.hero.sprite.get_width()
        self.score -= 0.02
        if self.map[self.hero.position[1]//step][self.hero.position[0]//step + 1] == Service.wall:
            return
        self.hero.position[0] += step
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
