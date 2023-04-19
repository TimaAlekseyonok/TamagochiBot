class Pet:
    def __init__(self, id, tipe, life_status, last_hp, hp, name, need_food, need_walk, need_wash, time):
        self.id = id
        self.tipe = tipe
        self.life_status = {'life_status': life_status, 'message': False}
        self.last_hp = last_hp
        self.hp = hp
        self.name = name
        self.need_food = {'need_food': need_food, 'message': False}
        self.need_walk = {'need_walk': need_walk, 'message': False}
        self.need_wash = {'need_wash': need_wash, 'message': False}
        self.time = time


    def food(self):
        self.need_food['need_food'] = True

    def walk(self):
        self.need_walk['need_walk'] = True

    def wash(self):
        self.need_wash['need_wash'] = True

    def got_food(self):
        self.need_food['need_food'] = False
        self.need_food['message'] = False

    def got_walk(self):
        self.need_walk['need_walk'] = False
        self.need_walk['message'] = False

    def got_wash(self):
        self.need_wash['need_wash'] = False
        self.need_wash['message'] = False

    def damage(self):
        if self.hp > 0:
            self.hp -= 1
        else:
            self.hp = 0
            self.life_status['life_status'] = False

    def heel(self):
        if self.hp < 10:
            self.hp += 1
        else:
            self.hp = 10



