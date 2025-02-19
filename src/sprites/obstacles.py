from src.sprites.game_sprites_parents import Obstacle

class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/brick.png")

    # ДОБАВИТЬ после пуль
    # def destroy():
    #     pass


class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/wall.png")

class Foliage(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/foliage.png")

class Base(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/base.png")