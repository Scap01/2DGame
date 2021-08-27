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
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #genrate a player
        player_position = tmx_data.get_object_by_name("Spawn")
        self.player = Player(player_position.x, player_position.y)

        #draw calque groupe
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer =3)
        self.group.add(self.player)


    def run(self):

        #game loop
        running = True

        while running:

            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()