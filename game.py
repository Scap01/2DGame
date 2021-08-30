import pygame
import pytmx
import pyscroll

from player import Player


class Game :
    def __init__(self):
        #creating game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2dg - beta")

        #load map (tmx)
        self.map = 'map'
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #genrate a player
        player_position = tmx_data.get_object_by_name("Spawn")
        self.player = Player(player_position.x, player_position.y)

        #define a list of collision objects

        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #draw calque groupe
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer =5)
        self.group.add(self.player)

        #define collistion rect for entrance

        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        #creating game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2dg - beta")

        #load map (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = 'house'

        #define a list of collision objects

        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #draw calque groupe
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer =5)
        self.group.add(self.player)

        #define collistion rect for entrance

        exit_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        #get spawn point in the house

        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        #creating game window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2dg - beta")

        #load map (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = 'map'

        #define a list of collision objects

        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #draw calque groupe
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer =5)
        self.group.add(self.player)

        #define collistion rect for entrance

        exit_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        #get spawn point outside the house

        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 10


    def update(self):
        self.group.update()

        #verification of house entrance collision

        if self.map == 'map' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        #verification of house entrance collision

        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'map'

        #verification of collision

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):

        clock = pygame.time.Clock()

        #game loop
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()