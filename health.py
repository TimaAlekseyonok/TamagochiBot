class Health:
    def __init__(self, health):
        self.health = health

    def __int__(self):
        return int(self.health)

    def damage(self):
        self.health -= 1
        return self.health

    def heel(self):
        if self.health < 10:
            self.health += 1
            return self.health





